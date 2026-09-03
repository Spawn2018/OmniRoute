from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "050_tracking_event_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_050_creates_tracking_event_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "050_tracking_event_rls"' in source
    assert 'down_revision: str | None = "049_shipment_rls"' in source
    assert '"tracking_event"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tracking_event_tenant_isolation" in source
    assert "uq_shipment_org_id" in source
    assert "fk_tracking_event_shipment" in source
    assert "eta" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tracking_service_does_not_import_shipments_or_quotes() -> None:
    service = (_SERVICES / "tracking_events" / "tracking_event_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.models.shipment" not in service
    assert "app.services.quotations" not in service
    assert "eta" not in service
    assert "httpx" not in service
    assert "leaflet" not in service


def test_importlinter_lists_tracking_events_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tracking_events" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tracking_events" in forbidden
    assert "app.models.tracking_event" in forbidden


def test_generated_api_types_include_tracking_event() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TrackingEventResponse" in source
    assert "TrackingEventCreate" in source
