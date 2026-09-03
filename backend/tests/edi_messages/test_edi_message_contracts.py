from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "053_edi_message_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_053_creates_edi_message_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "053_edi_message_rls"' in source
    assert 'down_revision: str | None = "052_operational_exception_rls"' in source
    assert '"edi_message"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "edi_message_tenant_isolation" in source
    assert "fk_edi_message_shipment" in source
    assert "x12" not in source.casefold()
    assert "edifact" not in source.casefold()
    assert "iftmin" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_edi_service_does_not_import_shipments_or_quotes() -> None:
    service = (_SERVICES / "edi_messages" / "edi_message_service.py").read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "from app.models.shipment import" not in service
    assert "app.services.quotations" not in service
    assert "app.services.channel_quotes" not in service
    assert "x12" not in service
    assert "httpx" not in service


def test_importlinter_lists_edi_messages_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.edi_messages" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.edi_messages" in forbidden
    assert "app.models.edi_message" in forbidden


def test_generated_api_types_include_edi_message() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "EdiMessageResponse" in source
    assert "EdiMessageCreate" in source
