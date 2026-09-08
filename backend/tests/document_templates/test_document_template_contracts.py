from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "102_document_template.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_102_creates_document_template_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "102_document_template"' in source
    assert 'down_revision: str | None = "101_pallet_balance"' in source
    assert '"document_template"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "document_template_tenant_isolation" in source
    assert "ix_document_template_org_kind" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_document_template_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "document_templates" / "document_template_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "app.services.networks" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_document_templates_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.document_templates" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.document_templates" in forbidden
    assert "app.models.document_template" in forbidden


def test_generated_api_types_include_document_template() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "DocumentTemplateResponse" in source
    assert "DocumentTemplateCreate" in source
