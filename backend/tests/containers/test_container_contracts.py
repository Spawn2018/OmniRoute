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


def test_generated_api_types_include_container() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ContainerResponse" in source
    assert "ContainerCreate" in source
    assert "seal_no_3" in source
    assert "vessel_name" in source
    assert "voyage_no" not in source
