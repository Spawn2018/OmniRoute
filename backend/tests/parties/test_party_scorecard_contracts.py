from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "021_party_scorecard_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_021_creates_party_scorecard_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "021_party_scorecard_rls"' in source
    assert 'down_revision: str | None = "020_network_rls"' in source
    assert '"party_scorecard"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "party_scorecard_tenant_isolation" in source
    assert "source_ref" in source
    assert "response_rate" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_pricing_and_extraction_do_not_import_party_scorecard() -> None:
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
            assert "party_scorecard" not in text
            assert "PartyScorecard" not in text


def test_generated_api_types_include_scorecard() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ScorecardResponse" in source
    assert "ScorecardUpsert" in source
