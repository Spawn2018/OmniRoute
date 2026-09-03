from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "039_outbox_event_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_039_creates_outbox_event_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "039_outbox_event_rls"' in source
    assert 'down_revision: str | None = "038_inbound_graph_ingest"' in source
    assert '"outbox_event"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "outbox_event_tenant_isolation" in source
    assert "inbound_message_saved" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_outbox_service_does_not_import_other_bc() -> None:
    service = (_SERVICES / "outbox_events" / "outbox_event_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.inbound_messages" not in service
    assert "app.services.quotations" not in service
    assert "app.services.extraction" not in service
    assert "app.services.mail_drafts" not in service
    assert "temporal" not in service.lower()
    assert "httpx" not in service
    assert "payload" not in service


def test_importlinter_lists_outbox_events_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.outbox_events" in independence


def test_generated_api_types_include_outbox_event() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OutboxEventResponse" in source or "OutboxEventCreate" in source
