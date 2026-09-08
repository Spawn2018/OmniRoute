from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "104_charge_template.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_104_creates_charge_template_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "104_charge_template"' in source
    assert 'down_revision: str | None = "103_rate_card"' in source
    assert '"charge_template"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "charge_template_tenant_isolation" in source
    assert "ix_charge_template_org_code" in source
    assert "btree_gist" not in source
    assert "EXCLUDE" not in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_charge_template_service_does_not_import_parents() -> None:
    service = (_SERVICES / "charge_templates" / "charge_template_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.charges" not in service
    assert "app.services.rate_cards" not in service
    assert "app.services.rate_lines" not in service
    assert "app.services.quotations" not in service
    assert "app.services.charge_codes" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "ChargeCodeRepository" in service


def test_importlinter_lists_charge_templates_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.charge_templates" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.charge_templates" in forbidden
    assert "app.models.charge_template" in forbidden


def test_generated_api_types_include_charge_template() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "ChargeTemplateResponse" in source
    assert "ChargeTemplateCreate" in source
