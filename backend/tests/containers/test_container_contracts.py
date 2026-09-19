from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "093_container.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_093_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "093_container"' in source
    assert 'down_revision: str | None = "092_trip"' in source
    assert '"container"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "container_tenant_isolation" in source
    assert "ix_container_org_type" in source
    assert "fk_container_shipment" in source
    assert "vgm_kg" not in source
    assert "buy_amount" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_shipments_or_charges() -> None:
    service = (_SERVICES / "containers" / "container_service.py").read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.parties" not in service
    assert "app.services.shipment_legs" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "app.services.stops" not in service
    assert "app.domain.stop" not in service
    assert "httpx" not in service


def test_importlinter_lists_containers_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.containers" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.containers" in forbidden
    assert "app.models.container" in forbidden


def test_migration_155_adds_seal_without_pin() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "155_container_seal.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "155_container_seal"' in source
    assert 'down_revision: str | None = "154_stop_notes"' in source
    assert "seal_no_1" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "seal_no_1" in source.split("def downgrade")[1]


def test_migration_156_adds_second_seal_without_pin() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "156_container_seal2.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "156_container_seal2"' in source
    assert 'down_revision: str | None = "155_container_seal"' in source
    assert "seal_no_2" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "seal_no_2" in source.split("def downgrade")[1]


def test_migration_157_adds_third_seal_without_pin() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "157_container_seal3.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "157_container_seal3"' in source
    assert 'down_revision: str | None = "156_container_seal2"' in source
    assert "seal_no_3" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "seal_no_3" in source.split("def downgrade")[1]


def test_migration_158_adds_vessel_without_voyage() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "158_container_vessel.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "158_container_vessel"' in source
    assert 'down_revision: str | None = "157_container_seal3"' in source
    assert "vessel_name" in source
    assert "voyage_no" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "vessel_name" in source.split("def downgrade")[1]


def test_migration_159_adds_voyage_without_booking() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "159_container_voyage.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "159_container_voyage"' in source
    assert 'down_revision: str | None = "158_container_vessel"' in source
    assert "voyage_no" in source
    assert "booking_no" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "voyage_no" in source.split("def downgrade")[1]


def test_migration_160_adds_remarks_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "160_container_remarks.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "160_container_remarks"' in source
    assert 'down_revision: str | None = "159_container_voyage"' in source
    assert "remarks" in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "remarks" in source.split("def downgrade")[1]


def test_migration_161_adds_cargo_description_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "161_container_cargo.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "161_container_cargo"' in source
    assert 'down_revision: str | None = "160_container_remarks"' in source
    assert "cargo_description" in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "cargo_description" in source.split("def downgrade")[1]


def test_migration_162_adds_packaging_code_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "162_container_pack.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "162_container_pack"' in source
    assert 'down_revision: str | None = "161_container_cargo"' in source
    assert "packaging_code" in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "packaging_code" in source.split("def downgrade")[1]


def test_migration_163_adds_ref_1_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "163_container_ref1.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "163_container_ref1"' in source
    assert 'down_revision: str | None = "162_container_pack"' in source
    assert "ref_1" in source
    assert "booking_no" not in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ref_1" in source.split("def downgrade")[1]


def test_migration_164_adds_ref_2_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "164_container_ref2.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "164_container_ref2"' in source
    assert 'down_revision: str | None = "163_container_ref1"' in source
    assert "ref_2" in source
    assert "booking_no" not in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ref_2" in source.split("def downgrade")[1]


def test_migration_165_adds_ref_3_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "165_container_ref3.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "165_container_ref3"' in source
    assert 'down_revision: str | None = "164_container_ref2"' in source
    assert "ref_3" in source
    assert "booking_no" not in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ref_3" in source.split("def downgrade")[1]


def test_migration_166_adds_ref_4_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "166_container_ref4.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "166_container_ref4"' in source
    assert 'down_revision: str | None = "165_container_ref3"' in source
    assert "ref_4" in source
    assert "booking_no" not in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ref_4" in source.split("def downgrade")[1]


def test_migration_167_adds_ref_5_without_weight() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "167_container_ref5.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "167_container_ref5"' in source
    assert 'down_revision: str | None = "166_container_ref4"' in source
    assert "ref_5" in source
    assert "booking_no" not in source
    assert "weight_kg" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ref_5" in source.split("def downgrade")[1]


def test_migration_168_adds_reefer_without_temperature() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "168_container_reefer.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "168_container_reefer"' in source
    assert 'down_revision: str | None = "167_container_ref5"' in source
    assert "reefer" in source
    assert "temp_min" not in source
    assert "temp_max" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "reefer" in source.split("def downgrade")[1]


def test_migration_169_adds_pickup_terminal_without_fk() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "169_container_pickup_terminal.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "169_container_pickup_terminal"' in source
    assert 'down_revision: str | None = "168_container_reefer"' in source
    assert "pickup_terminal" in source
    assert "pickup_terminal_id" not in source
    assert "carrier_party" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "pickup_terminal" in source.split("def downgrade")[1]


def test_migration_170_adds_return_terminal_without_fk() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "170_container_return_terminal.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "170_container_return_terminal"' in source
    assert 'down_revision: str | None = "169_container_pickup_terminal"' in source
    assert "return_terminal" in source
    assert "return_terminal_id" not in source
    assert "carrier_party" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "return_terminal" in source.split("def downgrade")[1]


def test_migration_171_adds_bl_kind_without_hbl() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "171_container_bl_kind.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "171_container_bl_kind"' in source
    assert 'down_revision: str | None = "170_container_return_terminal"' in source
    assert "bl_kind" in source
    assert "ocean_bill" not in source
    assert "hbl" not in source.casefold()
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "bl_kind" in source.split("def downgrade")[1]


def test_migration_172_adds_free_time_origin_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "172_container_free_time_origin.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "172_container_free_time_origin"' in source
    assert 'down_revision: str | None = "171_container_bl_kind"' in source
    assert "free_time_origin_h" in source
    assert "free_time_clock" not in source
    assert "countdown" not in source.casefold()
    assert "remaining" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "free_time_origin_h" in source.split("def downgrade")[1]


def test_migration_173_adds_free_time_dest_without_clock() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "173_container_free_time_dest.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "173_container_free_time_dest"' in source
    assert 'down_revision: str | None = "172_container_free_time_origin"' in source
    assert "free_time_dest_h" in source
    assert "free_time_clock" not in source
    assert "countdown" not in source
    assert "remaining" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "free_time_dest_h" in source.split("def downgrade")[1]


def test_migration_446_adds_demurrage_days_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "446_container_demurrage.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "446_container_demurrage"' in source
    assert 'down_revision: str | None = "445_blank_sailing_mark"' in source
    assert "demurrage_free_days" in source
    assert "countdown" not in source
    assert "remaining" not in source
    assert "free_time_clock" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "demurrage_free_days" in source.split("def downgrade")[1]


def test_migration_447_adds_detention_days_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "447_container_detention.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "447_container_detention"' in source
    assert 'down_revision: str | None = "446_container_demurrage"' in source
    assert "detention_free_days" in source
    assert "countdown" not in source
    assert "remaining" not in source
    assert "free_time_clock" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "detention_free_days" in source.split("def downgrade")[1]


def test_migration_448_adds_mixed_dd_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "448_container_mixed_dd.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "448_container_mixed_dd"' in source
    assert 'down_revision: str | None = "447_container_detention"' in source
    assert "mixed_dd_days" in source
    assert "countdown" not in source
    assert "remaining" not in source
    assert "free_time_clock" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "mixed_dd_days" in source.split("def downgrade")[1]


def test_migration_449_adds_tare_without_calculator() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "449_container_tare.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "449_container_tare"' in source
    assert 'down_revision: str | None = "448_container_mixed_dd"' in source
    assert "tare_kg" in source
    assert "Numeric(14, 4)" in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "tare_kg" in source.split("def downgrade")[1]


def test_migration_450_adds_pin_without_ciphertext() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "450_container_pin.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "450_container_pin"' in source
    assert 'down_revision: str | None = "449_container_tare"' in source
    assert "pin_code" in source
    assert "String(64)" in source
    assert "httpx" not in source
    assert "BYTEA" not in source
    assert "payload_kg" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "pin_code" in source.split("def downgrade")[1]


def test_migration_451_adds_payload_without_calculator() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "451_container_payload.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "451_container_payload"' in source
    assert 'down_revision: str | None = "450_container_pin"' in source
    assert "payload_kg" in source
    assert "Numeric(14, 4)" in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "payload_kg" in source.split("def downgrade")[1]
    assert "teu" not in source


def test_migration_452_adds_teu_without_iso_calculator() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "452_container_teu.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "452_container_teu"' in source
    assert 'down_revision: str | None = "451_container_payload"' in source
    assert "teu" in source
    assert "Numeric(14, 4)" in source
    assert "iso_size_type" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "teu" in source.split("def downgrade")[1]


def test_migration_453_adds_quantity_without_stop_write() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "453_container_quantity.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "453_container_quantity"' in source
    assert 'down_revision: str | None = "452_container_teu"' in source
    assert "quantity" in source
    assert "ck_container_quantity" in source
    assert "stop" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "quantity" in source.split("def downgrade")[1]
    assert "weight_kg" not in source


def test_migration_454_adds_weight_without_stop_write() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "454_container_weight.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "454_container_weight"' in source
    assert 'down_revision: str | None = "453_container_quantity"' in source
    assert "weight_kg" in source
    assert "Numeric(14, 4)" in source
    assert "stop" not in source
    assert "vgm_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "weight_kg" in source.split("def downgrade")[1]
    assert "volume_m3" not in source


def test_migration_455_adds_volume_without_cbm() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "455_container_volume.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "455_container_volume"' in source
    assert 'down_revision: str | None = "454_container_weight"' in source
    assert "volume_m3" in source
    assert "Numeric(14, 4)" in source
    assert "stop" not in source
    assert "weight_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "volume_m3" in source.split("def downgrade")[1]
    assert "pickup_date" not in source


def test_migration_456_adds_pickup_date_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "456_container_pickup_date.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "456_container_pickup_date"' in source
    assert 'down_revision: str | None = "455_container_volume"' in source
    assert "pickup_date" in source
    assert "Date()" in source
    assert "stop" not in source
    assert "volume_m3" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "pickup_date" in source.split("def downgrade")[1]
    assert "return_date" not in source


def test_migration_457_adds_return_date_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "457_container_return_date.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "457_container_return_date"' in source
    assert 'down_revision: str | None = "456_container_pickup_date"' in source
    assert "return_date" in source
    assert "Date()" in source
    assert "stop" not in source
    assert "pickup_date" not in source.split("def upgrade")[1]
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "return_date" in source.split("def downgrade")[1]
    assert "gate_in_date" not in source.split("def upgrade")[1]


def test_migration_458_adds_gate_in_date_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "458_container_gate_in_date.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "458_container_gate_in_date"' in source
    assert 'down_revision: str | None = "457_container_return_date"' in source
    assert "gate_in_date" in source
    assert "Date()" in source
    assert "stop" not in source
    assert "return_date" not in source.split("def upgrade")[1]
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "gate_in_date" in source.split("def downgrade")[1]
    assert "delivery_date" not in source.split("def upgrade")[1]


def test_migration_459_adds_delivery_date_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "459_container_delivery_date.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "459_container_delivery_date"' in source
    assert 'down_revision: str | None = "458_container_gate_in_date"' in source
    assert "delivery_date" in source
    assert "Date()" in source
    assert "stop" not in source
    assert "gate_in_date" not in source.split("def upgrade")[1]
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "delivery_date" in source.split("def downgrade")[1]
    assert "unload_date" not in source.split("def upgrade")[1]


def test_migration_460_adds_unload_date_without_countdown() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "460_container_unload_date.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "460_container_unload_date"' in source
    assert 'down_revision: str | None = "459_container_delivery_date"' in source
    assert "unload_date" in source
    assert "Date()" in source
    assert "stop" not in source
    assert "delivery_date" not in source.split("def upgrade")[1]
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "unload_date" in source.split("def downgrade")[1]
    assert "temp_min" not in source.split("def upgrade")[1]


def test_migration_461_adds_temp_min_without_float() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "461_container_temp_min.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "461_container_temp_min"' in source
    assert 'down_revision: str | None = "460_container_unload_date"' in source
    assert "temp_min" in source
    assert "Numeric(14, 4)" in source
    assert "temp_max" not in source.split("def upgrade")[1]
    assert "float" not in source.split("def upgrade")[1]
    assert "unload_date" not in source.split("def upgrade")[1]
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "temp_min" in source.split("def downgrade")[1]


def test_migration_174_adds_si_cutoff_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "174_container_si_cutoff.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "174_container_si_cutoff"' in source
    assert 'down_revision: str | None = "173_container_free_time_dest"' in source
    assert "si_cutoff_at" in source
    assert "ams_cutoff" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "si_cutoff_at" in source.split("def downgrade")[1]


def test_migration_175_adds_ams_cutoff_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "175_container_ams_cutoff.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "175_container_ams_cutoff"' in source
    assert 'down_revision: str | None = "174_container_si_cutoff"' in source
    assert "ams_cutoff_at" in source
    assert "cy_cutoff" not in source
    assert "cfs_cutoff" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "ams_cutoff_at" in source.split("def downgrade")[1]


def test_migration_176_adds_cy_cutoff_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "176_container_cy_cutoff.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "176_container_cy_cutoff"' in source
    assert 'down_revision: str | None = "175_container_ams_cutoff"' in source
    assert "cy_cutoff_at" in source
    assert "cfs_cutoff" not in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "vgm" not in source.casefold()
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "cy_cutoff_at" in source.split("def downgrade")[1]


def test_migration_177_adds_cfs_cutoff_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "177_container_cfs_cutoff.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "177_container_cfs_cutoff"' in source
    assert 'down_revision: str | None = "176_container_cy_cutoff"' in source
    assert "cfs_cutoff_at" in source
    assert "vgm" not in source.casefold()
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "cfs_cutoff_at" in source.split("def downgrade")[1]


def test_migration_178_adds_vgm_bundle_without_live_http() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "178_container_vgm.py").read_text(
        encoding="utf-8"
    )
    assert 'revision: str = "178_container_vgm"' in source
    assert 'down_revision: str | None = "177_container_cfs_cutoff"' in source
    assert "vgm_kg" in source
    assert "vgm_method" in source
    assert "vgm_cutoff_at" in source
    assert "Numeric(14, 4)" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "vgm_kg" in source.split("def downgrade")[1]


def test_migration_179_adds_last_survey_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "179_container_last_survey.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "179_container_last_survey"' in source
    assert 'down_revision: str | None = "178_container_vgm"' in source
    assert "last_survey_at" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "last_survey_at" in source.split("def downgrade")[1]


def test_migration_180_adds_booking_no_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "180_container_booking_no.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "180_container_booking_no"' in source
    assert 'down_revision: str | None = "179_container_last_survey"' in source
    assert "booking_no" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "booking_no" in source.split("def downgrade")[1]


def test_migration_181_adds_carrier_party_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "181_container_carrier_party.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "181_container_carrier_party"' in source
    assert 'down_revision: str | None = "180_container_booking_no"' in source
    assert "carrier_party_id" in source
    assert "fk_container_carrier_party" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "carrier_party_id" in source.split("def downgrade")[1]


def test_migration_182_adds_shipment_leg_without_live_http() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "182_container_shipment_leg.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "182_container_shipment_leg"' in source
    assert 'down_revision: str | None = "181_container_carrier_party"' in source
    assert "shipment_leg_id" in source
    assert "uq_shipment_leg_org_id" in source
    assert "fk_container_shipment_leg" in source
    assert "pin_code" not in source
    assert "payload_kg" not in source
    assert "httpx" not in source
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "shipment_leg_id" in source.split("def downgrade")[1]


def test_generated_api_types_include_container() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ContainerResponse" in source
    assert "ContainerCreate" in source
    assert "voyage_no" in source
    assert "remarks" in source
    assert "cargo_description" in source
    assert "packaging_code" in source
    assert "ref_1" in source
    assert "ref_2" in source
    assert "ref_3" in source
    assert "ref_4" in source
    assert "ref_5" in source
    assert "reefer" in source
    assert "pickup_terminal" in source
    assert "free_time_origin_h" in source
    assert "free_time_dest_h" in source
    assert "demurrage_free_days" in source
    assert "detention_free_days" in source
    assert "mixed_dd_days" in source
    assert "si_cutoff_at" in source
    assert "ams_cutoff_at" in source
    assert "cy_cutoff_at" in source
    assert "cfs_cutoff_at" in source
    assert "vgm_kg" in source
    assert "tare_kg" in source
    assert "pin_code" in source
    assert "payload_kg" in source
    assert "teu" in source
    assert "quantity" in source
    assert "weight_kg" in source
    assert "volume_m3" in source
    assert "pickup_date" in source
    assert "return_date" in source
    assert "gate_in_date" in source
    assert "delivery_date" in source
    assert "unload_date" in source
    assert "temp_min" in source
    assert "vgm_method" in source
    assert "vgm_cutoff_at" in source
    assert "last_survey_at" in source
    assert "booking_no" in source
    assert "carrier_party_id" in source
    assert "shipment_leg_id" in source
