from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "143_rank_mark.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_143_creates_rank_mark_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "143_rank_mark"' in source
    assert 'down_revision: str | None = "142_executive_mark"' in source
    assert '"rank_mark"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rank_mark_tenant_isolation" in source
    assert "uq_rank_mark_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_rank_mark_service_does_not_import_parents() -> None:
    service = (_SERVICES / "rank_marks" / "rank_mark_service.py").read_text(encoding="utf-8")
    assert "app.services.charges" not in service
    assert "app.services.networks" not in service
    assert "app.services.mail_drafts" not in service
    assert "app.services.extraction" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_rank_marks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.rank_marks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.rank_marks" in forbidden
    assert "app.models.rank_mark" in forbidden


def test_generated_api_types_include_rank_mark() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "RankMarkResponse" in source
    assert "RankMarkCreate" in source
