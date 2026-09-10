from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "198_plan_snapshot.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_198_creates_plan_snapshot_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "198_plan_snapshot"' in source
    assert 'down_revision: str | None = "197_outbox_task_template_kind"' in source
    assert '"plan_snapshot"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "plan_snapshot_tenant_isolation" in source
    assert "uq_plan_snapshot_org_source_ref" in source
    assert "uq_plan_snapshot_org_code" in source
    assert "fk_plan_snapshot_shipment" not in source
    assert "fk_plan_snapshot_trip" not in source
    assert "fk_plan_snapshot_resource" not in source
    assert '"shipment.id"' not in source
    assert '"trip.id"' not in source
    assert '"resource.id"' not in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "circle_sim" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_plan_snapshot_service_is_append_only_and_isolated() -> None:
    service = (_SERVICES / "plan_snapshots" / "plan_snapshot_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.trips" not in service
    assert "app.services.shipments" not in service
    assert "app.services.resources" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "buy_amount" not in service
    assert "circle_sim" not in service


def test_importlinter_lists_plan_snapshots_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.plan_snapshots" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.plan_snapshots" in forbidden
    assert "app.models.plan_snapshot" in forbidden


def test_generated_api_types_include_plan_snapshot() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "PlanSnapshotResponse" in source
    assert "PlanSnapshotCreate" in source
