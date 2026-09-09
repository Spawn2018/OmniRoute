from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "140_war_room_mark.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_140_creates_war_room_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "140_war_room_mark"' in source
    assert 'down_revision: str | None = "139_twin_mark"' in source
    assert '"war_room_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "war_room_mark_tenant_isolation" in source
    assert "uq_war_room_mark_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_war_room_mark_service_does_not_import_parents() -> None:
    service = (_SERVICES / "war_room_marks" / "war_room_mark_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.operational_exceptions" not in service
    assert "app.services.tower_impacts" not in service
    assert "app.services.extraction" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_war_room_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.war_room_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.war_room_marks" in forbidden
    assert "app.models.war_room_mark" in forbidden


def test_generated_api_types_include_war_room_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "WarRoomMarkResponse" in source
    assert "WarRoomMarkCreate" in source
