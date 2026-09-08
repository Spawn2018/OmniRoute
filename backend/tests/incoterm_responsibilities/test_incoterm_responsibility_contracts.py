from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "085_incoterm_responsibility.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_DOMAIN = _ROOT / "backend" / "app" / "domain" / "incoterm_responsibility.py"


def test_migration_085_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "085_incoterm_responsibility"' in source
    assert 'down_revision: str | None = "084_carry_checklist"' in source
    assert '"incoterm_responsibility"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "incoterm_responsibility_tenant_isolation" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "Incoterms®" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_quote_icc() -> None:
    service = (
        _SERVICES / "incoterm_responsibilities" / "incoterm_responsibility_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.quotations" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    domain = _DOMAIN.read_text(encoding="utf-8")
    assert "ICC" not in service
    assert "nie cytat tabeli ICC" in domain


def test_importlinter_lists_incoterm_responsibilities_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.incoterm_responsibilities" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.incoterm_responsibilities" in forbidden
    assert "app.models.incoterm_responsibility" in forbidden


def test_generated_api_types_include_incoterm_responsibility() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "IncotermResponsibilityResponse" in source
    assert "IncotermResponsibilityCreate" in source
