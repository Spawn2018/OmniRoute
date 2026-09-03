from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "070_fraud_flag_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_070_creates_fraud_flag_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "070_fraud_flag_rls"' in source
    assert 'down_revision: str | None = "069_cargo_claim_rls"' in source
    assert '"fraud_flag"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "fraud_flag_tenant_isolation" in source
    assert "fk_fraud_flag_party" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_fraud_flag_service_does_not_import_parents() -> None:
    service = (_SERVICES / "fraud_flags" / "fraud_flag_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.parties" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_fraud_flags_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.fraud_flags" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.fraud_flags" in forbidden
    assert "app.models.fraud_flag" in forbidden


def test_generated_api_types_include_fraud_flag() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "FraudFlagResponse" in source
    assert "FraudFlagCreate" in source
