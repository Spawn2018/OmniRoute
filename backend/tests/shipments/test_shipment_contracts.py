from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "049_shipment_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_049_creates_shipment_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "049_shipment_rls"' in source
    assert 'down_revision: str | None = "048_party_sanctions_screen"' in source
    assert '"shipment"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "shipment_tenant_isolation" in source
    assert "uq_quotation_org_id" in source
    assert "uq_shipment_org_quotation" in source
    assert "fk_shipment_quotation" in source
    assert "fk_shipment_party" in source
    assert "amount" not in source.casefold()
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_shipment_service_does_not_import_quotations_or_charges() -> None:
    service = (_SERVICES / "shipments" / "shipment_service.py").read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.models.quotation" not in service
    assert "app.services.document_templates" not in service
    assert "app.services.charges" not in service
    assert "app.services.nbp_rates" not in service
    assert "app.services.organization_calendars" not in service
    assert "app.services.operator_decisions" not in service
    assert "rate_line" not in service
    assert "amount" not in service
    assert "httpx" not in service
    assert "requests" not in service


def test_importlinter_lists_shipments_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.shipments" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.shipments" in forbidden
    assert "app.models.shipment" in forbidden


def test_generated_api_types_include_shipment() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "ShipmentResponse" in source
    assert "ShipmentCreate" in source


def test_migration_144_adds_shipment_ref_without_qr() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "144_shipment_ref.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "144_shipment_ref"' in source
    assert 'down_revision: str | None = "143_rank_mark"' in source
    assert "shipment_ref" in source
    assert "uq_shipment_org_shipment_ref" in source
    assert "qr" not in source.casefold()
    assert "pdf" not in source.casefold()
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source


def test_migration_444_adds_is_waste_without_mos() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "444_shipment_is_waste.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "444_shipment_is_waste"' in source
    assert 'down_revision: str | None = "443_waste_mark"' in source
    assert "is_waste" in source
    assert "Boolean" in source
    assert "httpx" not in source
    assert "Numeric" not in source
    assert "def downgrade" in source


def test_migration_500_adds_fx_anchor_dates_without_fx_sql() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "500_shipment_fx_anchor_dates.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "500_shipment_fx_anchor_dates"' in source
    assert 'down_revision: str | None = "499_document_template_branding"' in source
    assert "etd" in source
    assert "loading_date" in source
    assert "unloading_date" in source
    assert "invoice_date" in source
    assert "sa.Date()" in source
    assert "charge_sell_in_pln" not in source
    assert "nbp_rate" not in source
    assert "httpx" not in source
    assert "Numeric" not in source
    assert "def downgrade" in source


def test_migration_150_adds_parent_without_charge() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "150_shipment_parent.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "150_shipment_parent"' in source
    assert 'down_revision: str | None = "149_shipment_leg_air_waybill"' in source
    assert "parent_shipment_id" in source
    assert "relation_kind" in source
    assert "fk_shipment_parent" in source
    assert "ck_shipment_parent_pair" in source
    assert "ck_shipment_parent_not_self" in source
    assert "drayage" in source
    assert "charge" not in source.casefold()
    assert "margin" not in source.casefold()
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
