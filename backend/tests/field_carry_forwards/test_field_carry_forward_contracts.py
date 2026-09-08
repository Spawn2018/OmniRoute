from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "084_carry_checklist.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_084_creates_both_tables_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "084_carry_checklist"' in source
    assert 'down_revision: str | None = "083_inquiry_no_reply"' in source
    assert '"field_carry_forward"' in source
    assert '"document_checklist_rule"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "field_carry_forward_tenant_isolation" in source
    assert "document_checklist_rule_tenant_isolation" in source
    assert "fk_field_carry_forward_quotation" in source
    assert "fk_field_carry_forward_shipment" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_carry_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "field_carry_forwards" / "field_carry_forward_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_field_carry_forwards_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.field_carry_forwards" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.field_carry_forwards" in forbidden
    assert "app.models.field_carry_forward" in forbidden


def test_generated_api_types_include_field_carry_forward() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "FieldCarryForwardResponse" in source
    assert "FieldCarryForwardCreate" in source
