from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "213_otif_mark.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "otif_marks" / "otif_mark_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "otif_marks.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "otif_pct",
    "app.services.charges",
    "app.services.shipments",
    "app.services.stops",
    "app.services.extraction",
)


def test_migration_213_creates_otif_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "213_otif_mark"' in source
    assert 'down_revision: str | None = "212_routing_guide"' in source
    assert '"otif_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "otif_mark_tenant_isolation" in source
    assert "uq_otif_mark_org_source_ref" in source
    for banned in ("shipment_id", "otif_pct", "httpx", "float(", "currency"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_otif_mark_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source


def test_importlinter_lists_otif_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.otif_marks" in forbidden
    assert "app.models.otif_mark" in forbidden


def test_create_schema_forbids_shipment_and_metric_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "shipment_id" not in source
    assert "otif_pct" not in source
    assert "amount" not in source


def test_generated_api_types_include_otif_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OtifMarkResponse" in source
    assert "OtifMarkCreate" in source


def test_extraction_service_does_not_import_otif_mark() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "otif_mark" not in source
