from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "052_operational_exception_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_052_creates_operational_exception_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "052_operational_exception_rls"' in source
    assert 'down_revision: str | None = "051_shipment_document_rls"' in source
    assert '"operational_exception"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "operational_exception_tenant_isolation" in source
    assert "fk_operational_exception_shipment" in source
    assert "eta" not in source.casefold()
    assert "ais" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_exception_service_does_not_import_shipments_or_quotes() -> None:
    service = (
        _SERVICES / "operational_exceptions" / "operational_exception_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "from app.models.shipment import" not in service
    assert "app.services.quotations" not in service
    assert "eta" not in service
    assert "httpx" not in service


def test_importlinter_lists_operational_exceptions_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.operational_exceptions" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.operational_exceptions" in forbidden
    assert "app.models.operational_exception" in forbidden


def test_generated_api_types_include_operational_exception() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OperationalExceptionResponse" in source
    assert "OperationalExceptionCreate" in source
