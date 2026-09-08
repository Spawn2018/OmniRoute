from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "098_cod_instruction.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_098_creates_cod_instruction_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "098_cod_instruction"' in source
    assert 'down_revision: str | None = "097_dock_appointment"' in source
    assert '"cod_instruction"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "cod_instruction_tenant_isolation" in source
    assert "fk_cod_instruction_shipment" in source
    assert "ix_cod_instruction_org_shipment" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_cod_instruction_service_does_not_import_parents() -> None:
    service = (_SERVICES / "cod_instructions" / "cod_instruction_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "app.services.sales_invoices" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "Decimal" not in service


def test_importlinter_lists_cod_instructions_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.cod_instructions" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.cod_instructions" in forbidden
    assert "app.models.cod_instruction" in forbidden


def test_generated_api_types_include_cod_instruction() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CodInstructionResponse" in source
    assert "CodInstructionCreate" in source
