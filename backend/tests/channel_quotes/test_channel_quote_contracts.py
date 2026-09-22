from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "024_channel_quote_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_024_creates_channel_quote_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "024_channel_quote_rls"' in source
    assert 'down_revision: str | None = "023_port_surcharge_rls"' in source
    assert '"channel_quote"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "channel_quote_tenant_isolation" in source
    assert "source_ref" in source
    lowered = source.lower()
    assert "numeric(14, 4)" in lowered or "numeric(14,4)" in lowered
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_channel_quotes_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.channel_quotes" in independence


def test_pricing_and_extraction_do_not_import_channel_quotes() -> None:
    for bounded in ("quotations", "charges", "rate_lines", "extraction", "parties"):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "from app.services.channel_quotes" not in text
            assert "from app.repositories.channel_quotes" not in text
            assert "from app.models.channel_quote" not in text
            assert "app.services.channel_quotes" not in text


def test_generated_api_types_include_channel_quote() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ChannelQuoteResponse" in source
    assert "ChannelQuoteCreate" in source


def test_migration_493_adds_transport_mode() -> None:
    path = _ROOT / "backend" / "alembic" / "versions" / "493_channel_quote_transport_mode.py"
    source = path.read_text(encoding="utf-8")
    assert 'revision: str = "493_channel_quote_transport_mode"' in source
    assert "transport_mode" in source
    assert "uq_channel_quote_org_lane_day_mode" in source
    assert "ck_channel_quote_transport_mode" in source
    assert "air" in source and "other" in source
    assert "def downgrade" in source
