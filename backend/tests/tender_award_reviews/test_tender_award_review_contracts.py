from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "122_tender_award_review.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_122_creates_tender_award_review_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "122_tender_award_review"' in source
    assert 'down_revision: str | None = "121_tender_bid_stance"' in source
    assert '"tender_award_review"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tender_award_review_tenant_isolation" in source
    assert "ix_tender_award_review_org_code" in source
    assert "uq_tender_award_review_org_tender" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tender_award_review_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "tender_award_reviews" / "tender_award_review_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.tenders" not in service
    assert "app.services.tender_win_losses" not in service
    assert "app.services.operator_decisions" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_tender_award_reviews_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tender_award_reviews" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tender_award_reviews" in forbidden
    assert "app.models.tender_award_review" in forbidden


def test_generated_api_types_include_tender_award_review() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenderAwardReviewResponse" in source
    assert "TenderAwardReviewCreate" in source
