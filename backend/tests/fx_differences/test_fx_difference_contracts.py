from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "059_fx_difference_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_059_creates_fx_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "059_fx_difference_rls"' in source
    assert 'down_revision: str | None = "058_money_cost_rls"' in source
    assert '"fx_difference"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "fx_difference_tenant_isolation" in source
    assert "fk_fx_difference_quotation" in source
    assert "fk_fx_difference_rate" in source
    assert "uq_fx_difference_pair" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_fx_service_does_not_import_quotes_or_charges() -> None:
    service = (_SERVICES / "fx_differences" / "fx_difference_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.quotations" not in service
    assert "app.services.nbp_rates" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_fx_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.fx_differences" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.fx_differences" in forbidden
    assert "app.models.fx_difference" in forbidden


def test_generated_api_types_include_fx() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "FxDifferenceResponse" in source
    assert "FxDifferenceCreate" in source
