from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "019_dangerous_good_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_019_creates_dangerous_good_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "019_dangerous_good_rls"' in source
    assert 'down_revision: str | None = "018_nbp_rate_rls"' in source
    assert '"dangerous_good"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "dangerous_good_tenant_isolation" in source
    assert "ck_dangerous_good_un_digits" in source
    assert "source_ref" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_dangerous_goods_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.dangerous_goods" in independence


def test_pricing_and_extraction_do_not_import_dangerous_goods() -> None:
    for bounded in (
        "quotations",
        "charges",
        "rate_lines",
        "extraction",
        "commodity_codes",
        "nbp_rates",
    ):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "app.services.dangerous_goods" not in text
    for path in (_SERVICES / "extraction").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "dangerous_good" not in text


def test_generated_api_types_include_dangerous_good() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "DangerousGoodResponse" in source or "DangerousGoodCreate" in source
    assert "adr_tunnel_code" in source
    assert "segregation_group" in source


def test_migration_132_adds_adr_without_live_imo() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "132_dangerous_good_adr.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "132_dangerous_good_adr"' in source
    assert 'down_revision: str | None = "131_cargo_claim_cmr"' in source
    assert "adr_tunnel_code" in source
    assert "segregation_group" in source
    assert "httpx" not in source
    assert "buy_amount" not in source
    assert "def downgrade" in source
