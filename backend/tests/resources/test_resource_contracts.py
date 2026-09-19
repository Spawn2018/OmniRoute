from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "091_resource.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_091_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "091_resource"' in source
    assert 'down_revision: str | None = "090_stop"' in source
    assert '"resource"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "resource_tenant_isolation" in source
    assert "ix_resource_org_kind" in source
    assert "buy_amount" not in source
    assert "trip_id" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_465_adds_capacity_kg() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "465_resource_capacity_kg.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "465_resource_capacity_kg"' in source
    assert 'down_revision: str | None = "464_container_release"' in source
    assert "capacity_kg" in source
    assert "Numeric(14, 4)" in source
    assert "drop_column" in source.split("def downgrade")[1]


def test_migration_466_adds_capacity_ldm() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "466_resource_capacity_ldm.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "466_resource_capacity_ldm"' in source
    assert 'down_revision: str | None = "465_resource_capacity_kg"' in source
    assert "capacity_ldm" in source
    assert "Numeric(14, 4)" in source
    assert "drop_column" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_trip() -> None:
    service = (_SERVICES / "resources" / "resource_service.py").read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.parties" not in service
    assert "app.services.charges" not in service
    assert "app.services.stops" not in service
    assert "httpx" not in service


def test_importlinter_lists_resources_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.resources" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.resources" in forbidden
    assert "app.models.resource" in forbidden


def test_generated_api_types_include_resource() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ResourceResponse" in source
    assert "ResourceCreate" in source
