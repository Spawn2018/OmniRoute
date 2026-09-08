from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "105_fuel_index.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_105_creates_fuel_index_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "105_fuel_index"' in source
    assert 'down_revision: str | None = "104_charge_template"' in source
    assert '"fuel_index"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "fuel_index_tenant_isolation" in source
    assert "ix_fuel_index_org_kind" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_fuel_index_service_does_not_import_parents() -> None:
    service = (_SERVICES / "fuel_indexes" / "fuel_index_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.nbp_rates" not in service
    assert "app.services.charges" not in service
    assert "app.services.rate_cards" not in service
    assert "app.services.groupage_tariffs" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_fuel_indexes_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.fuel_indexes" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.fuel_indexes" in forbidden
    assert "app.models.fuel_index" in forbidden


def test_generated_api_types_include_fuel_index() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "FuelIndexResponse" in source
    assert "FuelIndexCreate" in source
