from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "195_consignment.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_195_creates_consignment_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "195_consignment"' in source
    assert 'down_revision: str | None = "194_trip_subcontractor"' in source
    assert '"consignment"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "consignment_tenant_isolation" in source
    assert "fk_consignment_shipment" in source
    assert "ix_consignment_org_shipment" in source
    assert "uq_consignment_org_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_consignment_service_does_not_import_parents() -> None:
    service = (_SERVICES / "consignments" / "consignment_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "app.services.shipment_packages" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "Decimal" not in service


def test_importlinter_lists_consignments_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.consignments" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.consignments" in forbidden
    assert "app.models.consignment" in forbidden


def test_generated_api_types_include_consignment() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "ConsignmentResponse" in source
    assert "ConsignmentCreate" in source
