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


def test_migration_042_creates_network_member_and_forces_rls() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "042_network_member_rls.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "042_network_member_rls"' in source
    assert 'down_revision: str | None = "041_mail_draft_sent"' in source
    assert '"network_member"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "network_member_tenant_isolation" in source


def test_network_service_has_no_scrape() -> None:
    service = (_SERVICES / "networks" / "network_service.py").read_text(encoding="utf-8")
    lowered = service.lower()
    assert "httpx" not in lowered
    assert "requests" not in lowered
    assert "scrap" not in lowered
    assert "app.services.parties" not in service


def test_member_list_joins_party_country_without_party_service() -> None:
    repo = (
        _ROOT / "backend" / "app" / "repositories" / "networks" / "network_member_repository.py"
    ).read_text(encoding="utf-8")
    assert "Party" in repo
    assert "country_code" in repo
    service = (_SERVICES / "networks" / "network_service.py").read_text(encoding="utf-8")
    assert "app.services.parties" not in service
    api = (_ROOT / "backend" / "app" / "api" / "networks.py").read_text(encoding="utf-8")
    assert "normalize_country_code" in api
    assert 'country_code: str | None = Query(default=None)' in api


def test_migration_073_adds_party_id_without_new_table() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "073_network_member_party.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "073_network_member_party"' in source
    assert "fk_network_member_party" in source
    assert "create_table" not in source.split("def upgrade")[1].split("def downgrade")[0]


def test_generated_api_types_include_network() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "NetworkResponse" in source or "NetworkCreate" in source
