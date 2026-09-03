from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "065_shipment_leg_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_065_creates_shipment_leg_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "065_shipment_leg_rls"' in source
    assert 'down_revision: str | None = "064_gdpr_request_rls"' in source
    assert '"shipment_leg"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_leg_tenant_isolation" in source
    assert "fk_shipment_leg_shipment" in source
    assert "fk_shipment_leg_origin" in source
    assert "fk_shipment_leg_destination" in source
    assert "uq_shipment_leg_org_kind" in source
    assert "ck_shipment_leg_kind" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_shipment_leg_service_does_not_import_parents() -> None:
    service = (_SERVICES / "shipment_legs" / "shipment_leg_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.geography" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_shipment_leg_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipment_legs" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipment_legs" in forbidden
    assert "app.models.shipment_leg" in forbidden


def test_generated_api_types_include_shipment_leg() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentLegResponse" in source
    assert "ShipmentLegCreate" in source


def test_migration_066_widens_leg_kind_to_rail() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "066_shipment_leg_rail_kind.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "066_shipment_leg_rail_kind"' in source
    assert 'down_revision: str | None = "065_shipment_leg_rls"' in source
    assert "leg_kind IN ('road', 'rail')" in source
    assert "drop_constraint" in source
    assert "create_table" not in source
    assert "httpx" not in source


def test_migration_067_widens_leg_kind_to_china_rail() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "067_shipment_leg_china_rail_kind.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "067_shipment_leg_china_rail_kind"' in source
    assert 'down_revision: str | None = "066_shipment_leg_rail_kind"' in source
    assert "leg_kind IN ('road', 'rail', 'china_rail')" in source
    assert "drop_constraint" in source
    assert "create_table" not in source
    assert "httpx" not in source


def test_migration_068_widens_leg_kind_to_ocean_lcl() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "068_shipment_leg_ocean_lcl_kind.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "068_shipment_leg_ocean_lcl_kind"' in source
    assert 'down_revision: str | None = "067_shipment_leg_china_rail_kind"' in source
    assert "ocean_lcl" in source
    assert "drop_constraint" in source
    assert "create_table" not in source
    assert "httpx" not in source
