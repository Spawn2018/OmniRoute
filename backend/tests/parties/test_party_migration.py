from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "015_party_rls.py"
_TABLES = (
    "party",
    "party_contact",
    "party_bank_account",
    "party_email_domain",
    "party_charge_override",
    "carrier_profile",
)


def test_migration_015_creates_six_party_tables_alters_terminal_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "015_party_rls"' in source
    assert 'down_revision: str | None = "014_terminal_rls"' in source
    for table in _TABLES:
        assert f'"{table}"' in source
        assert "FORCE ROW LEVEL SECURITY" in source
        assert f"{table}_tenant_isolation" in source
    assert "operator_party_id" in source
    assert "fk_terminal_operator_party" in source
    assert "uq_party_org_id" in source
    assert "uq_party_org_country_tax_id" in source
    assert "fk_party_charge_override_charge_code" in source
    assert "ck_party_credit_pair" in source
    assert "ck_party_roles" in source
    assert "WITH CHECK" in source
    assert "def downgrade" in source
    downgrade = source.split("def downgrade")[1]
    assert "drop_table" in downgrade
    assert "operator_party_id" in downgrade


def test_conftest_registers_party_models_and_forces_their_rls() -> None:
    source = (_ROOT / "backend" / "tests" / "conftest.py").read_text(encoding="utf-8")
    assert "app.models.party" in source or "from app.models.party import" in source
    for table in _TABLES:
        assert table in source


def test_generated_api_types_include_party_and_operator_party_id() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "PartyResponse" in source
    assert "operator_party_id" in source
    assert "sanctions_list_ref" in source
    assert "PartyScreenSanctions" in source
    assert "eori" in source
    assert "duns" in source
    assert "is_sole_trader" in source


def test_migration_075_adds_jdg_parent_and_role_assignment() -> None:
    path = _ROOT / "backend" / "alembic" / "versions" / "075_party_roles_jdg.py"
    assert path.is_file()
    source = path.read_text(encoding="utf-8")
    assert 'revision: str = "075_party_roles_jdg"' in source
    assert 'down_revision: str | None = "074_party_business_ids"' in source
    assert "is_sole_trader" in source
    assert "parent_party_id" in source
    assert "party_role_assignment" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "subcontractor" in source
    assert "def downgrade" in source


def test_migration_074_adds_eori_duns_and_unique_tokens() -> None:
    path = _ROOT / "backend" / "alembic" / "versions" / "074_party_business_ids.py"
    assert path.is_file()
    source = path.read_text(encoding="utf-8")
    assert 'revision: str = "074_party_business_ids"' in source
    assert 'down_revision: str | None = "073_network_member_party"' in source
    assert "eori" in source
    assert "duns" in source
    assert "uq_party_org_vat_eu" in source
    assert "uq_party_org_eori" in source
    assert "uq_party_org_duns" in source
    assert "def downgrade" in source
    downgrade = source.split("def downgrade")[1]
    assert "drop_column" in downgrade
    assert "uq_party_org_eori" in downgrade


def test_parties_api_has_screen_sanctions_and_no_list_http() -> None:
    api = (_ROOT / "backend" / "app" / "api" / "parties.py").read_text(encoding="utf-8")
    assert "screen-sanctions" in api
    assert "sanctions_list_ref" in api
    assert "httpx" not in api
    assert "requests" not in api
    assert "risk_score" not in api


def test_migration_048_adds_sanctions_screen_without_score_or_limit() -> None:
    path = _ROOT / "backend" / "alembic" / "versions" / "048_party_sanctions_screen.py"
    assert path.is_file()
    source = path.read_text(encoding="utf-8")
    assert 'revision: str = "048_party_sanctions_screen"' in source
    assert 'down_revision: str | None = "047_review_bureau_ref"' in source
    assert "sanctions_list_ref" in source
    assert "sanctions_checked_at" in source
    lowered = source.lower()
    assert "score" not in lowered
    assert "credit_limit" not in lowered
    assert "ofac" not in lowered
    assert "def downgrade" in source
    assert "drop_column" in source.split("def downgrade")[1]
