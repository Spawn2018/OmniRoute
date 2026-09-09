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
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
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
    assert "vgm" not in source.casefold()
    assert "create_table" not in source
    assert "def downgrade" in source
    assert "free_time_dest_h" in source.split("def downgrade")[1]


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
