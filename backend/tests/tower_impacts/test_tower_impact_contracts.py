from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "138_tower_impact.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_138_creates_tower_impact_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "138_tower_impact"' in source
    assert 'down_revision: str | None = "137_telematics_connector"' in source
    assert '"tower_impact"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tower_impact_tenant_isolation" in source
    assert "uq_tower_impact_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "penalty" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tower_impact_service_does_not_import_parents() -> None:
    service = (_SERVICES / "tower_impacts" / "tower_impact_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.parties" not in service
    assert "app.services.extraction" not in service
    assert "app.services.watchtower" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "sla_clause" not in service
    assert "party_scorecard" not in service


def test_importlinter_lists_tower_impacts_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tower_impacts" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tower_impacts" in forbidden
    assert "app.models.tower_impact" in forbidden


def test_generated_api_types_include_tower_impact() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TowerImpactResponse" in source
    assert "TowerImpactCreate" in source
