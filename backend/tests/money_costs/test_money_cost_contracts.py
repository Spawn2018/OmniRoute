from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "058_money_cost_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_058_creates_cost_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "058_money_cost_rls"' in source
    assert 'down_revision: str | None = "057_bank_payment_rls"' in source
    assert '"money_cost"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "money_cost_tenant_isolation" in source
    assert "fk_money_cost_payment" in source
    assert "fk_money_cost_rate" in source
    assert "uq_money_cost_pair" in source
    assert "uq_bank_payment_org_id" in source
    assert "uq_nbp_rate_org_id" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cost_service_does_not_import_payments_or_charges() -> None:
    service = (_SERVICES / "money_costs" / "money_cost_service.py").read_text(encoding="utf-8")
    assert "app.services.bank_payments" not in service
    assert "app.services.nbp_rates" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_costs_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.money_costs" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.money_costs" in forbidden
    assert "app.models.money_cost" in forbidden


def test_generated_api_types_include_cost() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "MoneyCostResponse" in source
    assert "MoneyCostCreate" in source
