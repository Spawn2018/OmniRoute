from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "216_freight_audit_mark.py"
_SERVICE = (
    _ROOT
    / "backend"
    / "app"
    / "services"
    / "freight_audit_marks"
    / "freight_audit_mark_service.py"
)
_API = _ROOT / "backend" / "app" / "api" / "freight_audit_marks.py"


def test_migration_216_creates_freight_audit_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "216_freight_audit_mark"' in source
    assert 'down_revision: str | None = "215_capa_mark"' in source
    assert '"freight_audit_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "freight_audit_mark_tenant_isolation" in source


def test_freight_audit_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in ("httpx", "float(", "app.services.charges", "margin"):
        assert banned not in source
    assert "UPDATE" not in source


def test_importlinter_lists_freight_audit_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.freight_audit_marks" in forbidden
    assert "app.models.freight_audit_mark" in forbidden


def test_generated_api_types_include_freight_audit_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8"
    )
    assert "FreightAuditMarkResponse" in source
