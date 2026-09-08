from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "076_entity_event.py"
_SERVICE = _ROOT / "backend" / "app" / "services" / "entity_events" / "entity_event_service.py"


def test_migration_076_creates_entity_event_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "076_entity_event"' in source
    assert 'down_revision: str | None = "075_party_roles_jdg"' in source
    assert '"entity_event"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "entity_event_tenant_isolation" in source
    assert "inquiry_queued" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_entity_event_service_is_append_only_and_isolated() -> None:
    service = _SERVICE.read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.services.carrier_inquiries" not in service
    assert "app.services.channel_quotes" not in service
    assert "app.services.outbox_events" not in service
    assert "temporal" not in service.lower()
    assert "httpx" not in service
    assert "payload" not in service
    assert ".update(" not in service
    assert "delete(" not in service.lower()
    assert "UPDATE" not in service
    assert "DELETE" not in service


def test_importlinter_lists_entity_events_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.entity_events" in independence


def test_generated_api_types_include_entity_event() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "EntityEventResponse" in source or "EntityEventCreate" in source
