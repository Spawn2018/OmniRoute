from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "106_local_charge.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_106_creates_local_charge_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "106_local_charge"' in source
    assert 'down_revision: str | None = "105_fuel_index"' in source
    assert '"local_charge"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "local_charge_tenant_isolation" in source
    assert "ix_local_charge_org_kind" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_local_charge_service_does_not_import_parents() -> None:
    service = (_SERVICES / "local_charges" / "local_charge_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.port_surcharges" not in service
    assert "app.services.channel_quotes" not in service
    assert "app.services.charges" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "app.services.geography" not in service
    assert "app.services.containers" not in service


def test_importlinter_lists_local_charges_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.local_charges" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.local_charges" in forbidden
    assert "app.models.local_charge" in forbidden


def test_generated_api_types_include_local_charge() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "LocalChargeResponse" in source
    assert "LocalChargeCreate" in source


def test_migration_147_adds_optional_port_unlocode() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "147_local_charge_port.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "147_local_charge_port"' in source
    assert 'down_revision: str | None = "146_charge_template_span"' in source
    assert "port_unlocode" in source
    assert "uq_local_charge_org_kind_port" in source
    assert "httpx" not in source
    assert "def downgrade" in source


def test_migration_148_adds_optional_iso_size_type() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "148_local_charge_iso.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "148_local_charge_iso"' in source
    assert 'down_revision: str | None = "147_local_charge_port"' in source
    assert "iso_size_type" in source
    assert "uq_local_charge_org_kind_port_type" in source
    assert "httpx" not in source
    assert "def downgrade" in source
