from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = (
    _ROOT / "backend" / "alembic" / "versions" / "217_collaboration_mark.py"
)
_SERVICE = (
    _ROOT
    / "backend"
    / "app"
    / "services"
    / "collaboration_marks"
    / "collaboration_mark_service.py"
)


def test_migration_217_creates_collaboration_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "217_collaboration_mark"' in source
    assert 'down_revision: str | None = "216_freight_audit_mark"' in source
    assert '"collaboration_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "collaboration_mark_tenant_isolation" in source


def test_collaboration_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in ("httpx", "float(", "app.services.charges", "shipment_stakeholder"):
        assert banned not in source
    assert "UPDATE" not in source


def test_importlinter_lists_collaboration_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.collaboration_marks" in forbidden
    assert "app.models.collaboration_mark" in forbidden


def test_generated_api_types_include_collaboration_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8"
    )
    assert "CollaborationMarkResponse" in source
