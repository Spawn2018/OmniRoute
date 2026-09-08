from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "087_document_dispatch_rule.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_087_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "087_document_dispatch_rule"' in source
    assert 'down_revision: str | None = "086_shipment_stakeholder"' in source
    assert '"document_dispatch_rule"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "document_dispatch_rule_tenant_isolation" in source
    assert "ix_document_dispatch_rule_org_triple" in source
    assert "buy_amount" not in source
    assert "mail_draft" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_send() -> None:
    service = (
        _SERVICES / "document_dispatch_rules" / "document_dispatch_rule_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.services.shipments" not in service
    assert "app.services.mail_drafts" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_document_dispatch_rules_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.document_dispatch_rules" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.document_dispatch_rules" in forbidden
    assert "app.models.document_dispatch_rule" in forbidden


def test_generated_api_types_include_document_dispatch_rule() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "DocumentDispatchRuleResponse" in source
    assert "DocumentDispatchRuleCreate" in source
