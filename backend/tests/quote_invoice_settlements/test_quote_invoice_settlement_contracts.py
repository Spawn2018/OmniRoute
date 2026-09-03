from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "056_quote_invoice_settlement_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_056_creates_settlement_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "056_quote_invoice_settlement_rls"' in source
    assert 'down_revision: str | None = "055_sales_invoice_ksef_ref"' in source
    assert '"quote_invoice_settlement"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "quote_invoice_settlement_tenant_isolation" in source
    assert "fk_quote_invoice_settlement_quotation" in source
    assert "fk_quote_invoice_settlement_invoice" in source
    assert "uq_quote_invoice_settlement_pair" in source
    assert "sell_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_settlement_service_does_not_import_quotes_or_charges() -> None:
    service = (
        _SERVICES / "quote_invoice_settlements" / "quote_invoice_settlement_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.services.sales_invoices" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "sell_amount" not in service


def test_importlinter_lists_settlements_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.quote_invoice_settlements" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.quote_invoice_settlements" in forbidden
    assert "app.models.quote_invoice_settlement" in forbidden


def test_generated_api_types_include_settlement() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "QuoteInvoiceSettlementResponse" in source
    assert "QuoteInvoiceSettlementCreate" in source
