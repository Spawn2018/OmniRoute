from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "211_asn.py"
_GUIDE_MIG = _ROOT / "backend" / "alembic" / "versions" / "219_asn_guide_code.py"
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
    "app.services.routing_guides",
    "app.services.routing_guide_enforcements",
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


def test_migration_219_adds_nullable_guide_code() -> None:
    source = _GUIDE_MIG.read_text(encoding="utf-8")
    assert 'revision: str = "219_asn_guide_code"' in source
    assert 'down_revision: str | None = "218_routing_guide_enforcement"' in source
    assert "guide_code" in source
    assert "ck_asn_guide_code" in source
    assert "drop_column" in source.split("def downgrade")[1]


def test_asn_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source
    assert "delete(" not in source
    assert ".update(" not in source


def test_api_composes_routing_gate_without_service_import_in_bc() -> None:
    api = _API.read_text(encoding="utf-8")
    assert "RoutingGuideEnforcementService" in api
    assert "RoutingGuideService" in api
    assert "RoutingGuideMatchService" in api
    assert "assert_asn_on_routing_guide" in api
    assert "assert_asn_labels_on_routing_guide" in api
    assert "guide_code" in api
    service = _SERVICE.read_text(encoding="utf-8")
    assert "routing_guide" not in service


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
