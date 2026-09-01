from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "022_customer_sop_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_022_creates_customer_sop_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "022_customer_sop_rls"' in source
    assert 'down_revision: str | None = "021_party_scorecard_rls"' in source
    assert '"customer_sop"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "customer_sop_tenant_isolation" in source
    assert "source_ref" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_pricing_and_extraction_do_not_import_customer_sop() -> None:
    for bounded in (
        "quotations",
        "charges",
        "rate_lines",
        "extraction",
        "commodity_codes",
        "nbp_rates",
        "dangerous_goods",
        "networks",
    ):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "customer_sop" not in text
            assert "CustomerSop" not in text


def test_generated_api_types_include_customer_sop() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CustomerSopResponse" in source
    assert "CustomerSopCreate" in source
