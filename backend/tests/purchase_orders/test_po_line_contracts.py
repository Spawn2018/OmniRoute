from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "210_po_line.py"
_SERVICE = _ROOT / "backend" / "app" / "services" / "purchase_orders" / "po_line_service.py"
_API = _ROOT / "backend" / "app" / "api" / "po_lines.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "app.services.charges",
    "app.services.shipments",
    "app.services.field_carry_forwards",
    "app.services.extraction",
)


def test_migration_210_creates_po_line_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "210_po_line"' in source
    assert 'down_revision: str | None = "209_purchase_order"' in source
    assert '"po_line"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "po_line_tenant_isolation" in source
    assert "uq_po_line_org_source_ref" in source
    assert "uq_po_line_org_header_line" in source
    assert "Numeric(14, 4)" in source
    assert "purchase_order_id" in source
    for banned in ("asn", "buy_amount", "httpx", "float(", "shipment_id", "currency"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_po_line_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source
    assert "delete(" not in source
    assert ".update(" not in source


def test_importlinter_lists_po_line_model_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.purchase_orders" in forbidden
    assert "app.models.po_line" in forbidden


def test_create_schema_forbids_asn_and_money_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "asn" not in source
    assert "shipment_id" not in source
    assert "amount" not in source
    assert "currency" not in source


def test_generated_api_types_include_po_line() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "PoLineResponse" in source
    assert "PoLineCreate" in source


def test_extraction_service_does_not_import_po_line() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "po_line" not in source
        assert "app.models.po_line" not in source
