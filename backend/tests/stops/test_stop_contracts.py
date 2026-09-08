from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "090_stop.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_090_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "090_stop"' in source
    assert 'down_revision: str | None = "089_organization_calendar"' in source
    assert '"stop"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "stop_tenant_isolation" in source
    assert "fk_stop_shipment" in source
    assert "fk_stop_location" in source
    assert "buy_amount" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_map() -> None:
    service = (_SERVICES / "stops" / "stop_service.py").read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.geography" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "leaflet" not in service


def test_importlinter_lists_stops_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.stops" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.stops" in forbidden
    assert "app.models.stop" in forbidden


def test_generated_api_types_include_stop() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "StopResponse" in source
    assert "StopCreate" in source
