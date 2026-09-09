from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "120_tender_prospect.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_120_creates_tender_prospect_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "120_tender_prospect"' in source
    assert 'down_revision: str | None = "119_extraction_draft_tender_rfp"' in source
    assert '"tender_prospect"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tender_prospect_tenant_isolation" in source
    assert "ix_tender_prospect_org_tender" in source
    assert "uq_tender_prospect_org_tender_party" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tender_prospect_service_does_not_import_parents() -> None:
    service = (_SERVICES / "tender_prospects" / "tender_prospect_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.tenders" not in service
    assert "app.services.parties" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_tender_prospects_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tender_prospects" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tender_prospects" in forbidden
    assert "app.models.tender_prospect" in forbidden


def test_generated_api_types_include_tender_prospect() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenderProspectResponse" in source
    assert "TenderProspectCreate" in source
