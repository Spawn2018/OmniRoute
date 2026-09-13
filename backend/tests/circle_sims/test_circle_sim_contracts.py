from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "199_circle_sim.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_199_creates_circle_sim_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "199_circle_sim"' in source
    assert 'down_revision: str | None = "198_plan_snapshot"' in source
    assert '"circle_sim"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "circle_sim_tenant_isolation" in source
    assert "uq_circle_sim_org_source_ref" in source
    assert "uq_circle_sim_org_code" in source
    assert "uq_circle_sim_org_pair" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "loaded_km" not in source
    assert "empty_km" not in source
    assert "approach_km" not in source
    assert "n_overlap" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_circle_sim_service_is_catalog_and_isolated() -> None:
    service = (_SERVICES / "circle_sims" / "circle_sim_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.trips" not in service
    assert "app.services.shipments" not in service
    assert "app.services.resources" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "app.services.tenders" not in service
    assert "httpx" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "buy_amount" not in service
    assert "loaded_km" not in service


def test_importlinter_lists_circle_sims_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.circle_sims" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.circle_sims" in forbidden
    assert "app.models.circle_sim" in forbidden
    assert "app.models.circle_sim_pair" in forbidden


def test_migration_359_adds_pair_view() -> None:
    source = (_ROOT / "backend/alembic/versions/359_circle_pair.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "359_circle_pair"' in source
    assert 'down_revision: str | None = "358_cf_run_snap"' in source
    assert "security_invoker = true" in source
    assert "CREATE VIEW circle_sim_pair" in source
    assert "a.id < b.id" in source
    assert "amount" not in source
    assert "loaded_km" not in source
    assert "n_overlap" not in source
    assert "float(" not in source.lower()


def test_generated_api_types_include_circle_sim() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "CircleSimResponse" in source
    assert "CircleSimCreate" in source
