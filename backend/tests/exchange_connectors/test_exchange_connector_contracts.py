from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "204_exchange_connector.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_SESSION = _ROOT / "backend" / "app" / "api" / "session.py"


def test_migration_204_creates_exchange_connector_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "204_exchange_connector"' in source
    assert 'down_revision: str | None = "203_idp_connector"' in source
    assert '"exchange_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "exchange_connector_tenant_isolation" in source
    assert "uq_exchange_connector_org_source_ref" in source
    assert "uq_exchange_connector_org_code" in source
    assert "trans_eu" in source
    assert "buy_amount" not in source
    assert "client_secret" not in source
    assert "ciphertext" not in source
    assert "base_url" not in source
    assert "httpx" not in source
    assert "float(" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_exchange_connector_service_is_catalog_and_isolated() -> None:
    service = (_SERVICES / "exchange_connectors" / "exchange_connector_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.networks" not in service
    assert "app.services.mail_drafts" not in service
    assert "app.services.outbox_events" not in service
    assert "app.services.idp_connectors" not in service
    assert "httpx" not in service
    assert "float(" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "client_secret" not in service


def test_session_login_is_untouched_by_exchange_catalog() -> None:
    source = _SESSION.read_text(encoding="utf-8")
    assert "exchange_connector" not in source
    assert "trans_eu" not in source
    assert "oauth" not in source.casefold()


def test_importlinter_lists_exchange_connectors_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.exchange_connectors" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.exchange_connectors" in forbidden
    assert "app.models.exchange_connector" in forbidden


def test_create_schema_forbids_secret_fields() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "exchange_connectors.py").read_text(
        encoding="utf-8",
    )
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "client_secret" not in source
    assert "ciphertext" not in source
    assert "base_url" not in source


def test_generated_api_types_include_exchange_connector() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "ExchangeConnectorResponse" in source
    assert "ExchangeConnectorCreate" in source
