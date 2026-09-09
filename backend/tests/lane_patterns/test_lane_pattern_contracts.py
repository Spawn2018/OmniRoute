from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "125_lane_pattern.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_125_creates_lane_pattern_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "125_lane_pattern"' in source
    assert 'down_revision: str | None = "124_tender_carbon_mark"' in source
    assert '"lane_pattern"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "lane_pattern_tenant_isolation" in source
    assert "ix_lane_pattern_org_origin" in source
    assert "uq_lane_pattern_org_pair" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "circle_sim" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_lane_pattern_service_does_not_import_parents() -> None:
    service = (_SERVICES / "lane_patterns" / "lane_pattern_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.tenders" not in service
    assert "app.services.tender_lanes" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_lane_patterns_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.lane_patterns" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.lane_patterns" in forbidden
    assert "app.models.lane_pattern" in forbidden


def test_generated_api_types_include_lane_pattern() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "LanePatternResponse" in source
    assert "LanePatternCreate" in source
