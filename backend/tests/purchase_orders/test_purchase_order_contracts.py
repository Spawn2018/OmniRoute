from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "209_purchase_order.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "purchase_orders" / "purchase_order_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "purchase_orders.py"
_BANNED = (
    "httpx",
    "float(",
    "sku",
    "quantity",
    "shipment_id",
    "app.services.charges",
    "app.services.shipments",
    "app.services.field_carry_forwards",
    "app.services.extraction",
)


def test_migration_209_creates_purchase_order_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "209_purchase_order"' in source
    assert 'down_revision: str | None = "208_visibility_connector"' in source
    assert '"purchase_order"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "purchase_order_tenant_isolation" in source
    assert "uq_purchase_order_org_source_ref" in source
    assert "uq_purchase_order_org_code" in source
    assert "plant_label" in source
    for banned in ("po_line", "asn", "buy_amount", "httpx", "float(", "shipment_id"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_purchase_order_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source
    assert "delete(" not in source
    assert ".update(" not in source


def test_importlinter_lists_purchase_orders_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.purchase_orders" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.purchase_orders" in forbidden
    assert "app.models.purchase_order" in forbidden


def test_create_schema_forbids_line_and_money_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "sku" not in source
    assert "qty" not in source
    assert "asn" not in source
    assert "shipment_id" not in source
    assert "amount" not in source


def test_generated_api_types_include_purchase_order() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "PurchaseOrderResponse" in source
    assert "PurchaseOrderCreate" in source


def test_extraction_service_does_not_import_purchase_orders() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "purchase_order" not in source
        assert "app.services.purchase_orders" not in source
