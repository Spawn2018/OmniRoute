from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "017_commodity_code_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_017_creates_commodity_code_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "017_commodity_code_rls"' in source
    assert 'down_revision: str | None = "016_quotation_port_party"' in source
    assert '"commodity_code"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "commodity_code_tenant_isolation" in source
    assert "ck_commodity_code_digits" in source
    assert "source_ref" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_commodity_codes_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.commodity_codes" in independence


def test_pricing_and_extraction_do_not_import_commodity_codes() -> None:
    for bounded in ("quotations", "charges", "rate_lines", "extraction"):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "commodity_code" not in text
            assert "app.services.commodity_codes" not in text


def test_generated_api_types_include_commodity_code() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CommodityCodeResponse" in source or "CommodityCodeCreate" in source
