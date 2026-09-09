from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "137_telematics_connector.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_137_creates_telematics_connector_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "137_telematics_connector"' in source
    assert 'down_revision: str | None = "136_free_time_clock"' in source
    assert '"telematics_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "telematics_connector_tenant_isolation" in source
    assert "uq_telematics_connector_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "credential_ciphertext" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_telematics_connector_service_does_not_import_parents() -> None:
    service = (_SERVICES / "telematics_connectors" / "telematics_connector_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.resources" not in service
    assert "app.services.trips" not in service
    assert "app.services.charges" not in service
    assert "app.services.extraction" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "ciphertext" not in service


def test_importlinter_lists_telematics_connectors_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.telematics_connectors" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.telematics_connectors" in forbidden
    assert "app.models.telematics_connector" in forbidden


def test_generated_api_types_include_telematics_connector() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TelematicsConnectorResponse" in source
    assert "TelematicsConnectorCreate" in source
