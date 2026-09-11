from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "215_capa_mark.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "capa_marks" / "capa_mark_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "capa_marks.py"
_BANNED = (
    "httpx",
    "float(",
    "shipment_id",
    "workflow_id",
    "app.services.charges",
    "app.services.shipments",
    "app.services.war_room_marks",
    "app.services.extraction",
)


def test_migration_215_creates_capa_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "215_capa_mark"' in source
    assert 'down_revision: str | None = "214_sap_connector"' in source
    assert '"capa_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "capa_mark_tenant_isolation" in source
    assert "uq_capa_mark_org_source_ref" in source
    for banned in ("shipment_id", "workflow_id", "httpx", "float(", "currency"):
        assert banned not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_capa_mark_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in _BANNED:
        assert banned not in source
    assert "UPDATE" not in source
    assert "DELETE" not in source


def test_importlinter_lists_capa_mark_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.capa_marks" in forbidden
    assert "app.models.capa_mark" in forbidden


def test_create_schema_forbids_shipment_and_metric_fields() -> None:
    source = _API.read_text(encoding="utf-8")
    assert "extra=\"forbid\"" in source or "extra='forbid'" in source
    assert "shipment_id" not in source
    assert "workflow_id" not in source
    assert "amount" not in source


def test_generated_api_types_include_capa_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CapaMarkResponse" in source
    assert "CapaMarkCreate" in source


def test_extraction_service_does_not_import_capa_mark() -> None:
    extraction = _ROOT / "backend" / "app" / "services" / "extraction"
    for path in extraction.rglob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "capa_mark" not in source
