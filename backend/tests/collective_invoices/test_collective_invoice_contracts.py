from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "063_collective_invoice_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_063_creates_collective_invoice_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "063_collective_invoice_rls"' in source
    assert 'down_revision: str | None = "062_bookkeeping_rls"' in source
    assert '"collective_invoice"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "collective_invoice_tenant_isolation" in source
    assert "fk_collective_invoice_invoice" in source
    assert "fk_collective_invoice_shipment" in source
    assert "uq_collective_invoice_pair" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_collective_invoice_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "collective_invoices" / "collective_invoice_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.sales_invoices" not in service
    assert "app.services.shipments" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_collective_invoice_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.collective_invoices" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.collective_invoices" in forbidden
    assert "app.models.collective_invoice" in forbidden


def test_generated_api_types_include_collective_invoice() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CollectiveInvoiceResponse" in source
    assert "CollectiveInvoiceCreate" in source
