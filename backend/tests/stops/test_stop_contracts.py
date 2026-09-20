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
    assert "app.services.dock_appointments" not in service
    assert "app.services.free_time_clocks" not in service
    assert "app.services.shipment_documents" not in service
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
    assert "weigh_in_kg" in source
    assert "quantity" in source
    assert "packaging_code" in source
    assert "seal_in" in source
    assert "seal_out" in source
    assert "appointment_ref" in source
    assert "waiting_free_minutes" in source
    assert "waiting_started_at" in source
    assert "pod_quality" in source
    assert "no_show_at" in source


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


def test_migration_185_adds_pack_without_seal() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "185_stop_pack.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "185_stop_pack"' in source
    assert 'down_revision: str | None = "184_stop_quantity"' in source
    assert "packaging_code" in source
    assert "seal" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "packaging_code" in source.split("def downgrade")[1]


def test_migration_186_adds_seal_in_without_seal_out() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "186_stop_seal_in.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "186_stop_seal_in"' in source
    assert 'down_revision: str | None = "185_stop_pack"' in source
    assert "seal_in" in source
    assert 'sa.Column("seal_out"' not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "seal_in" in source.split("def downgrade")[1]


def test_migration_187_adds_seal_out_without_appointment() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "187_stop_seal_out.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "187_stop_seal_out"' in source
    assert 'down_revision: str | None = "186_stop_seal_in"' in source
    assert "seal_out" in source
    assert "appointment" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "seal_out" in source.split("def downgrade")[1]


def test_migration_188_adds_appointment_ref_without_dock_table() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "188_stop_appointment_ref.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "188_stop_appointment_ref"' in source
    assert 'down_revision: str | None = "187_stop_seal_out"' in source
    assert "appointment_ref" in source
    assert "no_show" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "appointment_ref" in source.split("def downgrade")[1]


def test_migration_189_adds_waiting_without_countdown() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "189_stop_waiting.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "189_stop_waiting"' in source
    assert 'down_revision: str | None = "188_stop_appointment_ref"' in source
    assert "waiting_free_minutes" in source
    assert "ck_stop_waiting_free" in source
    assert "countdown" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "waiting_free_minutes" in source.split("def downgrade")[1]


def test_migration_190_adds_waiting_started_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "190_stop_waiting_started.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "190_stop_waiting_started"' in source
    assert 'down_revision: str | None = "189_stop_waiting"' in source
    assert "waiting_started_at" in source
    assert "countdown" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "waiting_started_at" in source.split("def downgrade")[1]


def test_migration_191_adds_pod_quality_without_camera() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "191_stop_pod_quality.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "191_stop_pod_quality"' in source
    assert 'down_revision: str | None = "190_stop_waiting_started"' in source
    assert "pod_quality" in source
    assert "ck_stop_pod_quality" in source
    assert "camera" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "pod_quality" in source.split("def downgrade")[1]


def test_migration_479_adds_no_show_without_charge() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "479_stop_no_show_at.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "479_stop_no_show_at"' in source
    assert 'down_revision: str | None = "478_stop_appointment_status"' in source
    assert "no_show_at" in source
    assert "margin" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "no_show_at" in source.split("def downgrade")[1]


def test_migration_480_adds_weigh_in_without_vgm() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "480_stop_weigh_in.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "480_stop_weigh_in"' in source
    assert 'down_revision: str | None = "479_stop_no_show_at"' in source
    assert "weigh_in_kg" in source
    assert "ck_stop_weigh_in" in source
    assert "vgm_kg" not in source
    assert "create_table" not in source
    assert "leaflet" not in source
    assert "def downgrade" in source
    assert "weigh_in_kg" in source.split("def downgrade")[1]
