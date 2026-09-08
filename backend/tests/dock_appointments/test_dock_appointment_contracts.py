from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "097_dock_appointment.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_097_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "097_dock_appointment"' in source
    assert 'down_revision: str | None = "096_shipment_package"' in source
    assert '"dock_appointment"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "dock_appointment_tenant_isolation" in source
    assert "ix_dock_appointment_org_stop" in source
    assert "fk_dock_appointment_stop" in source
    assert "window_start_local" in source
    assert "window_end_local" in source
    assert "buy_amount" not in source
    assert "wms_id" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_shipments_or_quotes() -> None:
    service = (_SERVICES / "dock_appointments" / "dock_appointment_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.stops" not in service
    assert "app.services.geography" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_dock_appointments_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.dock_appointments" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.dock_appointments" in forbidden
    assert "app.models.dock_appointment" in forbidden


def test_generated_api_types_include_dock_appointment() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "DockAppointmentResponse" in source
    assert "DockAppointmentCreate" in source
