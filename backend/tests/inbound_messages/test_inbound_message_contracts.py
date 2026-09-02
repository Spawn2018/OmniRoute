from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "026_inbound_message_rls.py"
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
