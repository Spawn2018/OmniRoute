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
