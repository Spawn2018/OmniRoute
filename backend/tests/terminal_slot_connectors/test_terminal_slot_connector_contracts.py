from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "202_terminal_slot_connector.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_API = _ROOT / "backend" / "app" / "api" / "terminal_slot_connectors.py"


def test_migration_202_creates_slot_connector_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "202_terminal_slot_connector"' in source
    assert 'down_revision: str | None = "201_erp_connector"' in source
    assert '"terminal_slot_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "terminal_slot_connector_tenant_isolation" in source
    assert "uq_terminal_slot_connector_org_source_ref" in source
    assert "uq_terminal_slot_connector_org_code" in source
    assert "uq_terminal_slot_connector_org_terminal" in source
    assert "email_hitl" in source
    assert "opens_local" in source
    assert "cutoff_local" in source
    assert "confirmed" not in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "float(" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_slot_connector_service_is_catalog_and_isolated() -> None:
    service = (
        _SERVICES / "terminal_slot_connectors" / "terminal_slot_connector_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.dock_appointments" not in service
    assert "app.services.geography" not in service
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "float(" not in service
    assert "confirmed" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service


def test_create_schema_forbids_confirmed_field() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "confirmed" not in source


def test_importlinter_lists_slot_connectors_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.terminal_slot_connectors" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.terminal_slot_connectors" in forbidden
    assert "app.models.terminal_slot_connector" in forbidden


def test_generated_api_types_include_slot_connector() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TerminalSlotConnectorResponse" in source
    assert "TerminalSlotConnectorCreate" in source
