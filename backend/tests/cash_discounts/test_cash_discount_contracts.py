from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "129_cash_discount.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_129_creates_cash_discount_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "129_cash_discount"' in source
    assert 'down_revision: str | None = "128_party_document"' in source
    assert '"cash_discount"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cash_discount_tenant_isolation" in source
    assert "uq_cash_discount_org_invoice_kind" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cash_discount_service_does_not_import_parents() -> None:
    service = (_SERVICES / "cash_discounts" / "cash_discount_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.sales_invoices" not in service
    assert "app.services.bank_payments" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_cash_discounts_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.cash_discounts" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cash_discounts" in forbidden
    assert "app.models.cash_discount" in forbidden


def test_generated_api_types_include_cash_discount() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "CashDiscountResponse" in source
    assert "CashDiscountCreate" in source
