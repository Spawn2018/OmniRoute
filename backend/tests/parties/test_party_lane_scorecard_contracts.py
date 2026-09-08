from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "081_party_lane_scorecard.py"
_SERVICE = _ROOT / "backend" / "app" / "services" / "parties" / "party_service.py"


def test_migration_081_creates_lane_scorecard_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "081_party_lane_scorecard"' in source
    assert 'down_revision: str | None = "080_mail_draft_inquiry"' in source
    assert '"party_lane_scorecard"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "party_lane_scorecard_tenant_isolation" in source
    assert "uq_party_lane_scorecard_org_party_lane_window" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_party_service_does_not_import_buy_or_shipment_bc() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    assert "app.services.carrier_inquiries" not in source
    assert "app.services.shipments" not in source
    assert "app.services.channel_quotes" not in source
    assert "app.services.quotations" not in source
    assert "httpx" not in source


def test_generated_api_types_include_lane_scorecard() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "LaneScorecardResponse" in source
    assert "LaneScorecardUpsert" in source
