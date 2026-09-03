from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "057_bank_payment_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_057_creates_payment_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "057_bank_payment_rls"' in source
    assert 'down_revision: str | None = "056_quote_invoice_settlement_rls"' in source
    assert '"bank_payment"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "bank_payment_tenant_isolation" in source
    assert "fk_bank_payment_invoice" in source
    assert "fk_bank_payment_account" in source
    assert "uq_bank_payment_pair" in source
    assert "uq_party_bank_account_org_id" in source
    assert "sell_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_payment_service_does_not_import_invoices_or_charges() -> None:
    service = (_SERVICES / "bank_payments" / "bank_payment_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.sales_invoices" not in service
    assert "app.services.parties" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "sell_amount" not in service


def test_importlinter_lists_payments_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.bank_payments" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.bank_payments" in forbidden
    assert "app.models.bank_payment" in forbidden


def test_generated_api_types_include_payment() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "BankPaymentResponse" in source
    assert "BankPaymentCreate" in source
