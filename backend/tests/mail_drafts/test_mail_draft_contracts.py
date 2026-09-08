from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "036_mail_draft_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_036_creates_mail_draft_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "036_mail_draft_rls"' in source
    assert 'down_revision: str | None = "035_operator_notice_rls"' in source
    assert '"mail_draft"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "mail_draft_tenant_isolation" in source
    assert "mail_draft" in source
    assert "inbound_message" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_041_allows_sent_status() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "041_mail_draft_sent.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "041_mail_draft_sent"' in source
    assert 'down_revision: str | None = "040_inbound_imap_ingest"' in source
    assert "to_address" in source
    assert "sent" in source


def test_migration_080_allows_inquiry_subject_kind() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "080_mail_draft_inquiry.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "080_mail_draft_inquiry"' in source
    assert 'down_revision: str | None = "079_quotation_incoterm"' in source
    assert "carrier_inquiry" in source
    assert "extraction_draft" in source


def test_mail_draft_service_does_not_import_extract_or_inbound() -> None:
    service = (_SERVICES / "mail_drafts" / "mail_draft_service.py").read_text(
        encoding="utf-8",
    )
    lowered = service.lower()
    assert "app.services.extraction" not in service
    assert "app.services.inbound_messages" not in service
    assert "app.services.quotations" not in service
    assert "app.services.operator_decisions" not in service
    assert "app.services.parties" not in service
    assert "rate_line" not in service
    assert "amount" not in service
    assert "smtp" not in lowered
    assert "graph.microsoft" not in lowered
    assert "httpx" not in lowered


def test_importlinter_lists_mail_drafts_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.mail_drafts" in independence


def test_generated_api_types_include_mail_draft() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "MailDraftResponse" in source or "MailDraftCreate" in source
