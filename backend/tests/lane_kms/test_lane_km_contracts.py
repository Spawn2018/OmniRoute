from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "200_lane_km.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_200_creates_lane_km_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "200_lane_km"' in source
    assert 'down_revision: str | None = "199_circle_sim"' in source
    assert '"lane_km"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "lane_km_tenant_isolation" in source
    assert "uq_lane_km_org_source_ref" in source
    assert "uq_lane_km_org_code" in source
    assert "Numeric(14, 4)" in source
    assert "loaded_km" in source
    assert "empty_km" in source
    assert "approach_km" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "haversine" not in source
    assert "float(" not in source
    assert "n_overlap" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_lane_km_service_is_catalog_and_isolated() -> None:
    service = (_SERVICES / "lane_kms" / "lane_km_service.py").read_text(encoding="utf-8")
    assert "app.services.trips" not in service
    assert "app.services.shipments" not in service
    assert "app.services.resources" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "app.services.circle_sims" not in service
    assert "app.services.tenders" not in service
    assert "httpx" not in service
    assert "haversine" not in service
    assert "float(" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_lane_kms_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.lane_kms" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.lane_kms" in forbidden
    assert "app.models.lane_km" in forbidden


def test_generated_api_types_include_lane_km() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "LaneKmResponse" in source
    assert "LaneKmCreate" in source
