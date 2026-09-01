from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "018_nbp_rate_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_018_creates_nbp_rate_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "018_nbp_rate_rls"' in source
    assert 'down_revision: str | None = "017_commodity_code_rls"' in source
    assert '"nbp_rate"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "nbp_rate_tenant_isolation" in source
    assert "source_ref" in source
    lowered = source.lower()
    assert "numeric(14, 4)" in lowered or "numeric(14,4)" in lowered
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_nbp_rates_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.nbp_rates" in independence


def test_pricing_and_extraction_do_not_import_nbp_rates() -> None:
    for bounded in ("quotations", "charges", "rate_lines", "extraction"):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "nbp_rate" not in text
            assert "app.services.nbp_rates" not in text


def test_generated_api_types_include_nbp_rate() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "NbpRateResponse" in source or "NbpRateCreate" in source
