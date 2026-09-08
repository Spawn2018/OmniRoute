from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "115_tender_playbook.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_115_creates_tender_playbook_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "115_tender_playbook"' in source
    assert 'down_revision: str | None = "114_tender_matrix_cell"' in source
    assert '"tender_playbook"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tender_playbook_tenant_isolation" in source
    assert "ix_tender_playbook_org_tender" in source
    assert "buy_amount" not in source
    assert "win_loss" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tender_playbook_service_does_not_import_parents() -> None:
    service = (_SERVICES / "tender_playbooks" / "tender_playbook_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.tenders" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_tender_playbooks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tender_playbooks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tender_playbooks" in forbidden
    assert "app.models.tender_playbook" in forbidden


def test_generated_api_types_include_tender_playbook() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenderPlaybookResponse" in source
    assert "TenderPlaybookCreate" in source
