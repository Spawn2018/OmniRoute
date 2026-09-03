from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "049_shipment_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_049_creates_shipment_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "049_shipment_rls"' in source
    assert 'down_revision: str | None = "048_party_sanctions_screen"' in source
    assert '"shipment"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_tenant_isolation" in source
    assert "uq_quotation_org_id" in source
    assert "uq_shipment_org_quotation" in source
    assert "fk_shipment_quotation" in source
    assert "fk_shipment_party" in source
    assert "amount" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_shipment_service_does_not_import_quotations_or_charges() -> None:
    service = (_SERVICES / "shipments" / "shipment_service.py").read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.models.quotation" not in service
    assert "app.services.charges" not in service
    assert "app.services.operator_decisions" not in service
    assert "rate_line" not in service
    assert "amount" not in service
    assert "httpx" not in service
    assert "requests" not in service


def test_importlinter_lists_shipments_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipments" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipments" in forbidden
    assert "app.models.shipment" in forbidden


def test_generated_api_types_include_shipment() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentResponse" in source
    assert "ShipmentCreate" in source
