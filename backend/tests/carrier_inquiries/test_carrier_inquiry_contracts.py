from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "043_carrier_inquiry_rls.py"
_SERVICE = (
    _ROOT / "backend" / "app" / "services" / "carrier_inquiries" / "carrier_inquiry_service.py"
)


def test_migration_043_creates_carrier_inquiry_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "043_carrier_inquiry_rls"' in source
    assert 'down_revision: str | None = "042_network_member_rls"' in source
    assert '"carrier_inquiry"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "carrier_inquiry_tenant_isolation" in source
    assert "uq_network_member_org_id" in source
    assert "fk_carrier_inquiry_network_member" in source
    assert "ck_carrier_inquiry_status_draft" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_inquiry_service_stays_inside_own_bc() -> None:
    source = _SERVICE.read_text(encoding="utf-8")
    assert "app.services.networks" not in source
    assert "app.services.quotations" not in source
    assert "app.services.entity_events" not in source
    assert "app.services.channel_quotes" not in source
    assert "app.services.customer_rfqs" not in source
    assert "httpx" not in source
    assert "requests" not in source
    assert "scrap" not in source
    assert "rate_line" not in source
    assert "app.services.operator_notices" not in source
    assert "weekday" not in source
    assert "083_inquiry_no_reply" in (
        _ROOT / "backend" / "alembic" / "versions" / "083_inquiry_no_reply.py"
    ).read_text(encoding="utf-8")
    assert "078_carrier_inquiry_batch" in (
        _ROOT / "backend" / "alembic" / "versions" / "078_carrier_inquiry_batch.py"
    ).read_text(encoding="utf-8")
    ranking = (
        _ROOT
        / "backend"
        / "app"
        / "repositories"
        / "carrier_inquiries"
        / "carrier_inquiry_repository.py"
    ).read_text(encoding="utf-8")
    assert "func.count().filter" in ranking
    assert "answered" in ranking


def test_importlinter_lists_carrier_inquiries_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.carrier_inquiries" in independence


def test_generated_api_types_include_carrier_inquiry() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CarrierInquiryResponse" in source
