from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "119_extraction_draft_tender_rfp.py"
_ACCEPT = _ROOT / "backend" / "app" / "api" / "accept_extraction.py"
_SERVICE = _ROOT / "backend" / "app" / "services" / "extraction" / "extraction_service.py"


def test_migration_119_widens_draft_kind_check() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "119_extraction_draft_tender_rfp"' in source
    assert 'down_revision: str | None = "118_tender_rfp_intake"' in source
    assert "tender_rfp" in source
    assert "FORCE ROW LEVEL SECURITY" not in source
    assert "create_table" not in source
    assert "def downgrade" in source


def test_accept_api_writes_intake_extraction_service_does_not() -> None:
    accept = _ACCEPT.read_text(encoding="utf-8")
    service = _SERVICE.read_text(encoding="utf-8")
    assert "TenderRfpIntakeService" in accept
    assert "CarrierInquiryService" in accept
    assert "mark_answered" in accept
    assert "TenderRfpIntakeService" not in service
    assert "CarrierInquiryService" not in service
    assert "app.services.tenders" not in service
    assert "app.services.tender_rfp_intakes" not in service
    assert "app.services.carrier_inquiries" not in service
    assert "app.services.channel_quotes" not in service
    assert "httpx" not in accept
