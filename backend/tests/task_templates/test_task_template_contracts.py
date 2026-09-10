from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "196_task_template.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_196_creates_task_template_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "196_task_template"' in source
    assert 'down_revision: str | None = "195_consignment"' in source
    assert '"task_template"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "task_template_tenant_isolation" in source
    assert "uq_task_template_org_code" in source
    assert "uq_task_template_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_task_template_api_composes_outbox_after_save() -> None:
    api = (_ROOT / "backend" / "app" / "api" / "task_templates.py").read_text(
        encoding="utf-8",
    )
    assert "record_template_saved" in api
    assert "OutboxEventService" in api
    assert "outbox://task-template/" in api
    assert "httpx" not in api


def test_task_template_service_does_not_import_parents() -> None:
    service = (_SERVICES / "task_templates" / "task_template_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.shipments" not in service
    assert "app.services.outbox_events" not in service
    assert "app.services.extraction" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_task_templates_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.task_templates" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.task_templates" in forbidden
    assert "app.models.task_template" in forbidden


def test_generated_api_types_include_task_template() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "TaskTemplateResponse" in source
    assert "TaskTemplateCreate" in source
