from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "141_memory_edge.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_141_creates_memory_edge_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "141_memory_edge"' in source
    assert 'down_revision: str | None = "140_war_room_mark"' in source
    assert '"memory_edge"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "memory_edge_tenant_isolation" in source
    assert "uq_memory_edge_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_memory_edge_service_does_not_import_parents() -> None:
    service = (_SERVICES / "memory_edges" / "memory_edge_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.entity_events" not in service
    assert "app.services.extraction" not in service
    assert "app.services.war_room_marks" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_memory_edges_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.memory_edges" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.memory_edges" in forbidden
    assert "app.models.memory_edge" in forbidden


def test_generated_api_types_include_memory_edge() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "MemoryEdgeResponse" in source
    assert "MemoryEdgeCreate" in source
