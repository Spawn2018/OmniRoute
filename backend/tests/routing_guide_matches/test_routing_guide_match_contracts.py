from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = (
    _ROOT / "backend" / "alembic" / "versions" / "221_routing_guide_match.py"
)
_SERVICE = (
    _ROOT
    / "backend"
    / "app"
    / "services"
    / "routing_guide_matches"
    / "routing_guide_match_service.py"
)


def test_migration_221_creates_match_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "221_routing_guide_match"' in source
    assert 'down_revision: str | None = "220_shipment_guide_code"' in source
    assert '"routing_guide_match"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "routing_guide_match_tenant_isolation" in source


def test_match_service_is_catalog_and_isolated() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    for banned in ("httpx", "float(", "app.services.charges", "assert_asn"):
        assert banned not in source
    assert "UPDATE" not in source


def test_importlinter_lists_match_on_deny_list() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.routing_guide_matches" in forbidden
    assert "app.models.routing_guide_match" in forbidden


def test_generated_api_types_include_match() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8"
    )
    assert "RoutingGuideMatchResponse" in source
