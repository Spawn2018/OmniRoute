from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "100_ocean_bill.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_100_creates_ocean_bill_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "100_ocean_bill"' in source
    assert 'down_revision: str | None = "099_groupage_tariff"' in source
    assert '"ocean_bill"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "ocean_bill_tenant_isolation" in source
    assert "fk_ocean_bill_shipment" in source
    assert "ix_ocean_bill_org_shipment" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_494_makes_bill_no_nullable_with_partial_unique() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "494_ocean_bill_number_pool.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "494_ocean_bill_number_pool"' in source
    assert "nullable=True" in source
    assert "uq_ocean_bill_org_bill_no" in source
    assert "bill_no IS NOT NULL" in source
    assert "buy_amount" not in source


def test_ocean_bill_service_does_not_import_parents() -> None:
    service = (_SERVICES / "ocean_bills" / "ocean_bill_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "Decimal" not in service


def test_importlinter_lists_ocean_bills_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.ocean_bills" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.ocean_bills" in forbidden
    assert "app.models.ocean_bill" in forbidden


def test_generated_api_types_include_ocean_bill() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OceanBillResponse" in source
    assert "OceanBillCreate" in source
