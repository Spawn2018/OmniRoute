from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION_208 = _ROOT / "backend" / "alembic" / "versions" / "208_visibility_connector.py"
_MIGRATION_224 = (
    _ROOT / "backend" / "alembic" / "versions" / "224_visibility_connector_vendors.py"
)
_SERVICE = (
    _ROOT
    / "backend"
    / "app"
    / "services"
    / "visibility_connectors"
    / "visibility_connector_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "visibility_connectors.py"
_BANNED = (
    "httpx",
    "float(",
    "api_key",
    "ciphertext",
    "base_url",
    "app.services.charges",
    "app.services.tracking_events",
    "app.services.telematics_connectors",
    "app.services.extraction",
)


def test_migration_208_creates_visibility_connector_and_forces_rls() -> None:
    source = _MIGRATION_208.read_text(encoding="utf-8")
    assert 'revision: str = "208_visibility_connector"' in source
    assert 'down_revision: str | None = "207_tenant_contract_kek"' in source
    assert '"visibility_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "visibility_connector_tenant_isolation" in source
    assert "uq_visibility_connector_org_source_ref" in source
    assert "uq_visibility_connector_org_code" in source
    assert "p44" in source
    assert "fourkites" not in source
    assert "shippeo" not in source
    for banned in ("BYTEA", "buy_amount", "httpx", "float(", "api_key"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_224_expands_visibility_vendor_tokens() -> None:
    source = _MIGRATION_224.read_text(encoding="utf-8")
    assert 'revision: str = "224_visibility_connector_vendors"' in source
    assert 'down_revision: str | None = "223_shipment_asn_id"' in source
    assert "fourkites" in source
    assert "shippeo" in source
    assert "p44" in source
    assert "ck_visibility_connector_kind" in source
    for banned in ("httpx", "float(", "api_key", "BYTEA", "buy_amount"):
        assert banned not in source
    assert "def downgrade" in source


def test_visibility_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source
    assert "delete(" not in source
    assert ".update(" not in source


def test_importlinter_lists_visibility_connectors_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.visibility_connectors" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.visibility_connectors" in forbidden
    assert "app.models.visibility_connector" in forbidden


def test_create_schema_forbids_secret_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "api_key" not in source
    assert "ciphertext" not in source
    assert "base_url" not in source


def test_generated_api_types_include_visibility_connector() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "VisibilityConnectorResponse" in source
    assert "VisibilityConnectorCreate" in source
