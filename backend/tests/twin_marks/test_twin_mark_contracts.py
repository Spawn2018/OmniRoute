from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "139_twin_mark.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_139_creates_twin_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "139_twin_mark"' in source
    assert 'down_revision: str | None = "138_tower_impact"' in source
    assert '"twin_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "twin_mark_tenant_isolation" in source
    assert "uq_twin_mark_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "plan_snapshot" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_twin_mark_service_does_not_import_parents() -> None:
    service = (_SERVICES / "twin_marks" / "twin_mark_service.py").read_text(encoding="utf-8")
    assert "app.services.charges" not in service
    assert "app.services.resources" not in service
    assert "app.services.trips" not in service
    assert "app.services.extraction" not in service
    assert "app.services.twin_kinds" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "plan_snapshot" not in service


def test_importlinter_lists_twin_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.twin_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.twin_marks" in forbidden
    assert "app.models.twin_mark" in forbidden


def test_generated_api_types_include_twin_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TwinMarkResponse" in source
    assert "TwinMarkCreate" in source
