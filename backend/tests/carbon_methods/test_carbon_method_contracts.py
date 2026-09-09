from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "130_carbon_method.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_130_creates_carbon_method_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "130_carbon_method"' in source
    assert 'down_revision: str | None = "129_cash_discount"' in source
    assert '"carbon_method"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "carbon_method_tenant_isolation" in source
    assert "uq_carbon_method_org_code_version" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_carbon_method_service_does_not_import_parents() -> None:
    service = (_SERVICES / "carbon_methods" / "carbon_method_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.tenders" not in service
    assert "app.services.shipments" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_carbon_methods_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.carbon_methods" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.carbon_methods" in forbidden
    assert "app.models.carbon_method" in forbidden


def test_generated_api_types_include_carbon_method() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "CarbonMethodResponse" in source
    assert "CarbonMethodCreate" in source
