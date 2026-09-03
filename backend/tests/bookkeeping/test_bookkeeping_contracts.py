from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "062_bookkeeping_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_062_creates_bookkeeping_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "062_bookkeeping_rls"' in source
    assert 'down_revision: str | None = "061_cost_to_serve_rls"' in source
    assert '"bookkeeping"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "bookkeeping_tenant_isolation" in source
    assert "fk_bookkeeping_charge" in source
    assert "fk_bookkeeping_invoice" in source
    assert "uq_bookkeeping_pair" in source
    assert "uq_charge_org_id" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_bookkeeping_service_does_not_import_charges() -> None:
    service = (_SERVICES / "bookkeeping" / "bookkeeping_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.sales_invoices" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_bookkeeping_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.bookkeeping" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.bookkeeping" in forbidden
    assert "app.models.bookkeeping" in forbidden


def test_generated_api_types_include_bookkeeping() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "BookkeepingResponse" in source
    assert "BookkeepingCreate" in source
