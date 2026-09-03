from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "061_cost_to_serve_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_061_creates_cost_to_serve_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "061_cost_to_serve_rls"' in source
    assert 'down_revision: str | None = "060_cash_flow_rls"' in source
    assert '"cost_to_serve"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cost_to_serve_tenant_isolation" in source
    assert "fk_cost_to_serve_sop" in source
    assert "fk_cost_to_serve_quotation" in source
    assert "uq_cost_to_serve_pair" in source
    assert "uq_customer_sop_org_id" in source
    assert "buy_amount" not in source
    assert "hourly_rate" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cost_to_serve_service_does_not_import_parties_or_charges() -> None:
    service = (_SERVICES / "cost_to_serve" / "cost_to_serve_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.parties" not in service
    assert "app.services.quotations" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_cost_to_serve_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.cost_to_serve" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cost_to_serve" in forbidden
    assert "app.models.cost_to_serve" in forbidden


def test_generated_api_types_include_cost_to_serve() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CostToServeResponse" in source
    assert "CostToServeCreate" in source
