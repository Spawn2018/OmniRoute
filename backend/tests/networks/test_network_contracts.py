from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "020_network_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_020_creates_network_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "020_network_rls"' in source
    assert 'down_revision: str | None = "019_dangerous_good_rls"' in source
    assert '"network"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "network_tenant_isolation" in source
    assert "ck_network_code_snake" in source
    assert "source_ref" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_networks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.networks" in independence


def test_pricing_and_extraction_do_not_import_networks() -> None:
    for bounded in (
        "quotations",
        "charges",
        "rate_lines",
        "extraction",
        "parties",
        "commodity_codes",
        "nbp_rates",
        "dangerous_goods",
    ):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "app.services.networks" not in text
            assert "app.models.network" not in text


def test_generated_api_types_include_network() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "NetworkResponse" in source or "NetworkCreate" in source
