from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "096_shipment_package.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_096_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "096_shipment_package"' in source
    assert 'down_revision: str | None = "095_groupage_line"' in source
    assert '"shipment_package"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_package_tenant_isolation" in source
    assert "ix_shipment_package_org_shipment" in source
    assert "fk_shipment_package_stop" in source
    assert "uq_stop_org_shipment_id" in source
    assert "buy_amount" not in source
    assert "wms_id" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_shipments_or_quotes() -> None:
    service = (_SERVICES / "shipment_packages" / "shipment_package_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.stops" not in service
    assert "app.services.geography" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_shipment_packages_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipment_packages" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipment_packages" in forbidden
    assert "app.models.shipment_package" in forbidden


def test_generated_api_types_include_shipment_package() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentPackageResponse" in source
    assert "ShipmentPackageCreate" in source
