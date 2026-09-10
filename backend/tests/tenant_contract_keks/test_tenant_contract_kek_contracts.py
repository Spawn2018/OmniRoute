from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "207_tenant_contract_kek.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_CONTRACTS = _ROOT / "backend" / "app" / "services" / "customer_contracts"
_FORBIDDEN = (
    "BYTEA",
    "wrapped_dek",
    "client_secret",
    "ciphertext",
    "fernet",
    "AES",
    "httpx",
    "float(",
    "app.services.customer_contracts",
    "app.services.charges",
    "app.services.extraction",
)


def test_migration_207_creates_kek_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "207_tenant_contract_kek"' in source
    assert 'down_revision: str | None = "206_customer_contract_blob"' in source
    assert '"tenant_contract_kek"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tenant_contract_kek_tenant_isolation" in source
    assert "uq_tenant_contract_kek_org_source_ref" in source
    assert "uq_tenant_contract_kek_org_code" in source
    assert "password" in source
    assert "kms" in source
    for banned in ("BYTEA", "wrapped_dek", "buy_amount", "httpx", "float("):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_kek_mark_service_is_catalog_and_isolated() -> None:
    service = (_SERVICES / "tenant_contract_keks" / "tenant_contract_kek_service.py").read_text(
        encoding="utf-8",
    )
    for banned in _FORBIDDEN:
        assert banned not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service


def test_customer_contract_bc_stays_without_kek_columns() -> None:
    service = (_CONTRACTS / "customer_contract_service.py").read_text(encoding="utf-8")
    assert "tenant_contract_kek" not in service
    assert "wrapped_dek" not in service


def test_importlinter_lists_kek_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tenant_contract_keks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tenant_contract_keks" in forbidden
    assert "app.models.tenant_contract_kek" in forbidden


def test_create_schema_forbids_secret_fields() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "tenant_contract_keks.py").read_text(
        encoding="utf-8",
    )
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "password:" not in source
    assert "ciphertext" not in source
    assert "wrapped_dek" not in source


def test_generated_api_types_include_kek_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenantContractKekResponse" in source
    assert "TenantContractKekCreate" in source
