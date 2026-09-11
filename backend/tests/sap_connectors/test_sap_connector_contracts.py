from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "214_sap_connector.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "sap_connectors" / "sap_connector_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "sap_connectors.py"
_BANNED = (
    "httpx",
    "float(",
    "base_url",
    "api_key",
    "app.services.charges",
    "app.services.erp_connectors",
)


def test_migration_214_creates_sap_connector_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "214_sap_connector"' in source
    assert 'down_revision: str | None = "213_otif_mark"' in source
    assert '"sap_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "sap_connector_tenant_isolation" in source
    for banned in ("base_url", "api_key", "httpx", "float("):
        assert banned not in source


def test_sap_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source


def test_importlinter_lists_sap_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.sap_connectors" in forbidden
    assert "app.models.sap_connector" in forbidden


def test_create_schema_forbids_secret_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert 'extra="forbid"' in source or "extra='forbid'" in source
    assert "base_url" not in source
    assert "api_key" not in source


def test_generated_api_types_include_sap_connector() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "SapConnectorResponse" in source
    assert "SapConnectorCreate" in source


def test_extraction_service_does_not_import_sap_connector() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        assert "sap_connector" not in path.read_text(encoding="utf-8")
