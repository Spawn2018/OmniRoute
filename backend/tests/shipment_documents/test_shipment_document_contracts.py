from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "051_shipment_document_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_051_creates_shipment_document_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "051_shipment_document_rls"' in source
    assert 'down_revision: str | None = "050_tracking_event_rls"' in source
    assert '"shipment_document"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_document_tenant_isolation" in source
    assert "fk_shipment_document_shipment" in source
    assert "pdf" not in source.casefold()
    assert "hbl" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_496_adds_rod_kind_without_new_table() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "496_shipment_document_rod.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "496_shipment_document_rod"' in source
    assert 'down_revision: str | None = "495_pallet_balance_epal"' in source
    assert "rod" in source
    assert "create_table" not in source
    assert "httpx" not in source
    assert "pdf" not in source.casefold()


def test_document_service_does_not_import_shipments_or_quotes() -> None:
    service = (
        _SERVICES / "shipment_documents" / "shipment_document_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "from app.models.shipment import" not in service
    assert "app.services.quotations" not in service
    assert "app.services.extraction" not in service
    assert "pdf" not in service
    assert "httpx" not in service


def test_importlinter_lists_shipment_documents_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipment_documents" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipment_documents" in forbidden
    assert "app.models.shipment_document" in forbidden


def test_generated_api_types_include_shipment_document() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentDocumentResponse" in source
    assert "ShipmentDocumentCreate" in source
