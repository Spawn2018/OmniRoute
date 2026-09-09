from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "092_trip.py"
_FREEZE = _ROOT / "backend" / "alembic" / "versions" / "107_trip_expected_buy.py"
_DRIVER2 = _ROOT / "backend" / "alembic" / "versions" / "151_trip_driver2.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_092_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "092_trip"' in source
    assert 'down_revision: str | None = "091_resource"' in source
    assert '"trip"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "trip_tenant_isolation" in source
    assert "ix_trip_org_status" in source
    assert "fk_trip_vehicle" in source
    assert "uq_resource_org_id" in source
    assert "buy_amount" not in source
    assert "planned_distance" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_107_adds_expected_buy_without_variance() -> None:
    source = _FREEZE.read_text(encoding="utf-8")
    assert 'revision: str = "107_trip_expected_buy"' in source
    assert 'down_revision: str | None = "106_local_charge"' in source
    assert "expected_buy_amount" in source
    assert "expected_buy_currency" in source
    assert "ck_trip_expected_buy_freeze" in source
    assert "app.services.charges" not in source
    assert "variance" not in source
    assert "planned_distance" not in source
    assert "def downgrade" in source


def test_service_does_not_import_fleet_or_charges() -> None:
    service = (_SERVICES / "trips" / "trip_service.py").read_text(encoding="utf-8")
    assert "app.services.resources" not in service
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_trips_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.trips" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.trips" in forbidden
    assert "app.models.trip" in forbidden


def test_generated_api_types_include_trip() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TripResponse" in source
    assert "TripCreate" in source
    assert "driver2_id" in source
    assert "route_label" in source


def test_migration_153_adds_route_label_without_km() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "153_trip_route_label.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "153_trip_route_label"' in source
    assert 'down_revision: str | None = "152_stop_group"' in source
    assert "route_label" in source
    assert "planned_distance" not in source
    assert "app.services.charges" not in source
    assert "def downgrade" in source
    assert "route_label" in source.split("def downgrade")[1]


def test_migration_151_adds_driver2_without_km() -> None:
    source = _DRIVER2.read_text(encoding="utf-8")
    assert 'revision: str = "151_trip_driver2"' in source
    assert 'down_revision: str | None = "150_shipment_parent"' in source
    assert "driver2_id" in source
    assert "fk_trip_driver2" in source
    assert "ck_trip_driver2_distinct" in source
    assert "planned_distance" not in source
    assert "app.services.charges" not in source
    assert "def downgrade" in source
    assert "driver2_id" in source.split("def downgrade")[1]
