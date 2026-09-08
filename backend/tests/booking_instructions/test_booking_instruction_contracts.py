from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "088_booking_instruction.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_088_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "088_booking_instruction"' in source
    assert 'down_revision: str | None = "087_document_dispatch_rule"' in source
    assert '"booking_instruction"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "booking_instruction_tenant_isolation" in source
    assert "fk_booking_instruction_shipment" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_http() -> None:
    service = (
        _SERVICES / "booking_instructions" / "booking_instruction_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.incoterm_responsibilities" not in service
    assert "app.services.mail_drafts" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_booking_instructions_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.booking_instructions" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.booking_instructions" in forbidden
    assert "app.models.booking_instruction" in forbidden


def test_generated_api_types_include_booking_instruction() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "BookingInstructionResponse" in source
    assert "BookingInstructionCreate" in source
