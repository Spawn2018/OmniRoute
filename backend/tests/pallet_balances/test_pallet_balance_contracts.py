from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "101_pallet_balance.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_101_creates_pallet_balance_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "101_pallet_balance"' in source
    assert 'down_revision: str | None = "100_ocean_bill"' in source
    assert '"pallet_balance"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "pallet_balance_tenant_isolation" in source
    assert "fk_pallet_balance_party" in source
    assert "ix_pallet_balance_org_party" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_pallet_balance_service_does_not_import_parents() -> None:
    service = (_SERVICES / "pallet_balances" / "pallet_balance_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.parties" not in service
    assert "app.services.charges" not in service
    assert "app.services.shipments" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "Decimal" not in service


def test_importlinter_lists_pallet_balances_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.pallet_balances" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.pallet_balances" in forbidden
    assert "app.models.pallet_balance" in forbidden


def test_generated_api_types_include_pallet_balance() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "PalletBalanceResponse" in source
    assert "PalletBalanceCreate" in source
