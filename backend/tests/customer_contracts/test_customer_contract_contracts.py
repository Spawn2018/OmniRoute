from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "205_customer_contract.py"
_BLOB_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "206_customer_contract_blob.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_EXTRACTION = _SERVICES / "extraction"


def test_migration_205_creates_customer_contract_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "205_customer_contract"' in source
    assert 'down_revision: str | None = "204_exchange_connector"' in source
    assert '"customer_contract"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "customer_contract_tenant_isolation" in source
    assert "uq_customer_contract_org_source_ref" in source
    assert "uq_customer_contract_org_code" in source
    assert "buy_amount" not in source
    assert "blob_ciphertext" not in source
    assert "wrapped_dek" not in source
    assert "tenant_contract_kek" not in source
    assert "plaintext" not in source
    assert "httpx" not in source
    assert "float(" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_206_adds_nullable_blob_without_kek() -> None:
    source = _BLOB_MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "206_customer_contract_blob"' in source
    assert 'down_revision: str | None = "205_customer_contract"' in source
    assert "blob_ciphertext" in source
    assert "BYTEA" in source or "LargeBinary" in source
    assert "wrapped_dek" not in source
    assert "tenant_contract_kek" not in source
    assert "unwrap" not in source
    assert "Fernet" not in source
    assert "AES" not in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    assert "drop_column" in source.split("def downgrade")[1]


def test_customer_contract_service_is_catalog_and_isolated() -> None:
    service = (_SERVICES / "customer_contracts" / "customer_contract_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.parties" not in service
    assert "app.services.extraction" not in service
    assert "httpx" not in service
    assert "float(" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "wrapped_dek" not in service
    assert "tenant_contract_kek" not in service
    assert "def decrypt" not in service
    assert "unwrap" not in service
    assert "Fernet" not in service
    assert "AES" not in service


def test_extraction_service_does_not_import_customer_contracts() -> None:
    for path in _EXTRACTION.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "customer_contract" not in source
        assert "app.services.customer_contracts" not in source


def test_importlinter_lists_customer_contracts_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.customer_contracts" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.customer_contracts" in forbidden
    assert "app.models.customer_contract" in forbidden


def test_create_schema_forbids_contract_body_fields() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "customer_contracts.py").read_text(
        encoding="utf-8",
    )
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "blob_ciphertext" not in source
    assert "wrapped_dek" not in source
    assert "plaintext" not in source
    assert " body" not in source


def test_generated_api_types_include_customer_contract() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "CustomerContractResponse" in source
    assert "CustomerContractCreate" in source
    response = source.split("export type CustomerContractResponse")[1].split(
        "export type",
        1,
    )[0]
    assert "has_ciphertext" in response
    assert "blob_ciphertext" not in response
    assert "plaintext" not in response
