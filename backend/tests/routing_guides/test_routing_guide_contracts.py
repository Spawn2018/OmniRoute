from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "212_routing_guide.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "routing_guides" / "routing_guide_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "routing_guides.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "blocks_dispatch",
    "app.services.charges",
    "app.services.shipments",
    "app.services.trips",
    "app.services.extraction",
)


def test_migration_212_creates_routing_guide_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "212_routing_guide"' in source
    assert 'down_revision: str | None = "211_asn"' in source
    assert '"routing_guide"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "routing_guide_tenant_isolation" in source
    assert "uq_routing_guide_org_source_ref" in source
    for banned in ("shipment_id", "blocks_dispatch", "httpx", "float(", "currency"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_routing_guide_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source


def test_importlinter_lists_routing_guide_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.routing_guides" in forbidden
    assert "app.models.routing_guide" in forbidden


def test_create_schema_forbids_shipment_and_block_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "shipment_id" not in source
    assert "blocks_dispatch" not in source
    assert "amount" not in source


def test_generated_api_types_include_routing_guide() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "RoutingGuideResponse" in source
    assert "RoutingGuideCreate" in source


def test_extraction_service_does_not_import_routing_guide() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "routing_guide" not in source
