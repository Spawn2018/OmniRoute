from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "109_tender.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_109_creates_tender_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "109_tender"' in source
    assert 'down_revision: str | None = "108_tender_quote"' in source
    assert '"tender"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tender_tenant_isolation" in source
    assert "ix_tender_org_status" in source
    assert "buy_amount" not in source
    assert "tender_lot" not in source
    assert "auto_award" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tender_service_does_not_import_parents() -> None:
    service = (_SERVICES / "tenders" / "tender_service.py").read_text(encoding="utf-8")
    assert "app.services.parties" not in service
    assert "app.services.quotations" not in service
    assert "app.services.charges" not in service
    assert "app.services.tender_quotes" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_tenders_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tenders" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tenders" in forbidden
    assert "app.models.tender" in forbidden


def test_generated_api_types_include_tender() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenderResponse" in source
    assert "TenderCreate" in source
