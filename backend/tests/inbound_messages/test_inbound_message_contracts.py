from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "026_inbound_message_rls.py"
_MIGRATION_PARTY = _ROOT / "backend" / "alembic" / "versions" / "027_inbound_message_party.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_026_creates_inbound_message_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "026_inbound_message_rls"' in source
    assert 'down_revision: str | None = "025_credit_review_rls"' in source
    assert '"inbound_message"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "inbound_message_tenant_isolation" in source
    assert "ck_inbound_message_status_draft" in source
    assert "ck_inbound_message_source_fixture" in source
    assert "source_ref" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_027_adds_same_tenant_party_fk() -> None:
    source = _MIGRATION_PARTY.read_text(encoding="utf-8")
    assert 'revision: str = "027_inbound_message_party"' in source
    assert "fk_inbound_message_party" in source
    assert "party_id" in source
    assert "organization_id" in source


def test_inbound_service_does_not_import_parties_or_extraction() -> None:
    service = (
        _ROOT
        / "backend"
        / "app"
        / "services"
        / "inbound_messages"
        / "inbound_message_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.parties" not in service
    assert "app.models.party" not in service
    assert "app.services.extraction" not in service
    assert "app.models.extraction_draft" not in service
    assert "app.services.quotations" not in service
    assert "app.services.mail_drafts" not in service
    assert "app.services.operator_decisions" not in service


def test_importlinter_lists_inbound_messages_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.inbound_messages" in independence


def test_pricing_and_extraction_do_not_import_inbound_messages() -> None:
    for bounded in (
        "quotations",
        "charges",
        "rate_lines",
        "extraction",
        "parties",
        "commodity_codes",
        "nbp_rates",
        "dangerous_goods",
        "networks",
    ):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "app.services.inbound_messages" not in text
            assert "app.models.inbound_message" not in text


def test_generated_api_types_include_inbound_message() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "InboundMessageResponse" in source or "InboundMessageCreate" in source
    assert "InboundExtractResponse" in source


def test_service_has_no_graph_or_imap() -> None:
    service = (
        _ROOT
        / "backend"
        / "app"
        / "services"
        / "inbound_messages"
        / "inbound_message_service.py"
    ).read_text(encoding="utf-8")
    lowered = service.lower()
    assert "graph.microsoft" not in lowered
    assert "imap" not in lowered
    assert "httpx" not in lowered


def test_migration_040_adds_mailbox_prefix() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "040_inbound_imap_ingest.py"
    ).read_text(encoding="utf-8")
    assert "imap" in source
    assert "039_outbox_event_rls" in source


def test_migration_038_adds_graph_external_id() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "038_inbound_graph_ingest.py"
    ).read_text(encoding="utf-8")
    assert "external_id" in source
    assert "graph" in source
    assert "037_operator_decision_lock" in source


def test_migration_421_adds_rfc822_headers() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "421_inbound_rfc822.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "421_inbound_rfc822"' in source
    assert 'down_revision: str | None = "420_trip_bill_mark"' in source
    assert "rfc822_message_id" in source
    assert "in_reply_to" in source
    assert "ix_inbound_message_org_rfc822" in source
    assert "FORCE ROW LEVEL SECURITY" not in source


def test_inbound_extract_api_does_not_accept_rates() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "inbound_messages.py").read_text(
        encoding="utf-8",
    )
    assert "extract_to_draft" in source
    assert "AcceptExtractionToRates" not in source
    assert "rate_line" not in source
