from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "086_shipment_stakeholder.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_086_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "086_shipment_stakeholder"' in source
    assert 'down_revision: str | None = "085_incoterm_responsibility"' in source
    assert '"shipment_stakeholder"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_stakeholder_tenant_isolation" in source
    assert "fk_shipment_stakeholder_shipment" in source
    assert "fk_shipment_stakeholder_party" in source
    assert "buy_amount" not in source
    assert "sold_to" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "shipment_stakeholders" / "shipment_stakeholder_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.parties" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_shipment_stakeholders_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipment_stakeholders" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipment_stakeholders" in forbidden
    assert "app.models.shipment_stakeholder" in forbidden


def test_generated_api_types_include_shipment_stakeholder() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentStakeholderResponse" in source
    assert "ShipmentStakeholderCreate" in source
