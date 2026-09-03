from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "054_sales_invoice_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_054_creates_sales_invoice_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "054_sales_invoice_rls"' in source
    assert 'down_revision: str | None = "053_edi_message_rls"' in source
    assert '"sales_invoice"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "sales_invoice_tenant_isolation" in source
    assert "fk_sales_invoice_shipment" in source
    assert "ksef" not in source.casefold()
    assert "sell_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_sales_invoice_service_does_not_import_shipments_or_charges() -> None:
    service = (_SERVICES / "sales_invoices" / "sales_invoice_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "from app.models.shipment import" not in service
    assert "app.services.charges" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "xml" not in service
    assert "note_ksef" in service


def test_importlinter_lists_sales_invoices_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.sales_invoices" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.sales_invoices" in forbidden
    assert "app.models.sales_invoice" in forbidden


def test_generated_api_types_include_sales_invoice() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "SalesInvoiceResponse" in source
    assert "SalesInvoiceCreate" in source
    assert "SalesInvoiceKsefNote" in source


def test_migration_055_adds_ksef_ref_without_xml() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "055_sales_invoice_ksef_ref.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "055_sales_invoice_ksef_ref"' in source
    assert 'down_revision: str | None = "054_sales_invoice_rls"' in source
    assert "ksef_ref" in source
    assert "ksef_noted_at" in source
    assert "xml" not in source.casefold()
    assert "fa3" not in source
    assert "httpx" not in source
    assert "drop_column" in source.split("def downgrade")[1]
