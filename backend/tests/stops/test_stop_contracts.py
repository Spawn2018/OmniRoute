from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "090_stop.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_090_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "090_stop"' in source
    assert 'down_revision: str | None = "089_organization_calendar"' in source
    assert '"stop"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "stop_tenant_isolation" in source
    assert "fk_stop_shipment" in source
    assert "fk_stop_location" in source
    assert "buy_amount" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_map() -> None:
    service = (_SERVICES / "stops" / "stop_service.py").read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.geography" not in service
    assert "app.services.charges" not in service
    assert "app.services.containers" not in service
    assert "httpx" not in service
    assert "leaflet" not in service
    assert "open-meteo" not in service.casefold()
    assert "gps" not in service.casefold()


def test_migration_134_adds_eta_clocks() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "134_stop_eta.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "134_stop_eta"' in source
    assert 'down_revision: str | None = "133_prediction_ledger"' in source
    assert "eta_physical" in source
    assert "eta_legal" in source
    assert "DateTime(timezone=True)" in source
    assert "created_at" in source
    assert "leaflet" not in source
    assert "open-meteo" not in source.casefold()
    assert "def downgrade" in source
    assert "drop_column" in source.split("def downgrade")[1]


def test_importlinter_lists_stops_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.stops" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.stops" in forbidden
    assert "app.models.stop" in forbidden


def test_generated_api_types_include_stop() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "StopResponse" in source
    assert "notes_for_driver" in source
    assert "weight_kg" in source
    assert "quantity" in source


def test_migration_152_adds_group_code_without_table() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "152_stop_group.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "152_stop_group"' in source
    assert 'down_revision: str | None = "151_trip_driver2"' in source
    assert "stop_group_code" in source
    assert "ck_stop_group_code" in source
    assert "create_table" not in source
    assert "planned_distance" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "stop_group_code" in source.split("def downgrade")[1]


def test_migration_154_adds_notes_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "154_stop_notes.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "154_stop_notes"' in source
    assert 'down_revision: str | None = "153_trip_route_label"' in source
    assert "notes_for_driver" in source
    assert "weight" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "notes_for_driver" in source.split("def downgrade")[1]


def test_migration_183_adds_weight_without_vgm() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "183_stop_weight.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "183_stop_weight"' in source
    assert 'down_revision: str | None = "182_container_shipment_leg"' in source
    assert "weight_kg" in source
    assert "vgm" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "weight_kg" in source.split("def downgrade")[1]


def test_migration_184_adds_quantity_without_packaging() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "184_stop_quantity.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "184_stop_quantity"' in source
    assert 'down_revision: str | None = "183_stop_weight"' in source
    assert "quantity" in source
    assert "packaging" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "quantity" in source.split("def downgrade")[1]
