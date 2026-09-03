from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "060_cash_flow_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_060_creates_cash_flow_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "060_cash_flow_rls"' in source
    assert 'down_revision: str | None = "059_fx_difference_rls"' in source
    assert '"cash_flow"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cash_flow_tenant_isolation" in source
    assert "fk_cash_flow_quotation" in source
    assert "fk_cash_flow_payment" in source
    assert "uq_cash_flow_pair" in source
    assert "buy_amount" not in source
    assert "sell_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cash_flow_service_does_not_import_quotes_or_charges() -> None:
    service = (_SERVICES / "cash_flows" / "cash_flow_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.quotations" not in service
    assert "app.services.bank_payments" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "sell_amount" not in service


def test_importlinter_lists_cash_flow_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.cash_flows" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cash_flows" in forbidden
    assert "app.models.cash_flow" in forbidden


def test_generated_api_types_include_cash_flow() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CashFlowResponse" in source
    assert "CashFlowCreate" in source
