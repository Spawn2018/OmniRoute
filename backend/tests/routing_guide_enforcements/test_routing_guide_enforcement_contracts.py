from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = (
    _ROOT / "backend" / "alembic" / "versions" / "218_routing_guide_enforcement.py"
)
_SERVICE = (
    _ROOT
    / "backend"
    / "app"
    / "services"
    / "routing_guide_enforcements"
    / "routing_guide_enforcement_service.py"
)


def test_migration_218_creates_routing_guide_enforcement_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "218_routing_guide_enforcement"' in source
    assert 'down_revision: str | None = "217_collaboration_mark"' in source
    assert '"routing_guide_enforcement"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "routing_guide_enforcement_tenant_isolation" in source
    assert "record_only" in source
    assert "block_409" in source


def test_enforcement_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in (
        "httpx",
        "float(",
        "app.services.charges",
        "app.services.shipments",
        "app.services.routing_guides",
        "UPDATE",
    ):
        assert banned not in source


def test_importlinter_lists_enforcement_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.routing_guide_enforcements" in forbidden
    assert "app.models.routing_guide_enforcement" in forbidden


def test_generated_api_types_include_routing_guide_enforcement() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8"
    )
    assert "RoutingGuideEnforcementResponse" in source
