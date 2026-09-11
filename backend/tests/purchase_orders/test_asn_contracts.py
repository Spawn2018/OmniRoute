from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "211_asn.py"
_SERVICE = _ROOT / "backend" / "app" / "services" / "purchase_orders" / "asn_service.py"
_API = _ROOT / "backend" / "app" / "api" / "asns.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "app.services.charges",
    "app.services.shipments",
    "app.services.field_carry_forwards",
    "app.services.edi_messages",
    "app.services.extraction",
)


def test_migration_211_creates_asn_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "211_asn"' in source
    assert 'down_revision: str | None = "210_po_line"' in source
    assert '"asn"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "asn_tenant_isolation" in source
    assert "uq_asn_org_source_ref" in source
    assert "uq_asn_org_header_code" in source
    assert "purchase_order_id" in source
    for banned in ("shipment_id", "buy_amount", "httpx", "float(", "currency", "payload"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_asn_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source
    assert "delete(" not in source
    assert ".update(" not in source


def test_importlinter_lists_asn_model_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.purchase_orders" in forbidden
    assert "app.models.asn" in forbidden


def test_create_schema_forbids_shipment_and_money_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "shipment_id" not in source
    assert "amount" not in source
    assert "currency" not in source
    assert "payload" not in source


def test_generated_api_types_include_asn() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "AsnResponse" in source
    assert "AsnCreate" in source


def test_extraction_service_does_not_import_asn() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "app.models.asn" not in source
        assert "asn_service" not in source
