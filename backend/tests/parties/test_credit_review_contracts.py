from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "025_credit_review_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_MODEL = _ROOT / "backend" / "app" / "models" / "credit_review.py"


def test_migration_025_creates_credit_review_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "025_credit_review_rls"' in source
    assert 'down_revision: str | None = "024_channel_quote_rls"' in source
    assert '"credit_review"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "credit_review_tenant_isolation" in source
    assert "source_ref" in source
    assert "uq_credit_review_org_party_day" in source
    assert "fk_credit_review_party" in source
    assert "ok" in source and "hold" in source and "refuse" in source
    lowered = source.lower()
    assert "score" not in lowered
    assert "rating" not in lowered
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_model_has_no_score_column() -> None:
    source = _MODEL.read_text(encoding="utf-8")
    assert "score" not in source.lower()
    assert "rating" not in source.lower()
    assert "credit_limit" not in source


def test_pricing_and_extraction_do_not_import_credit_review() -> None:
    for bounded in (
        "quotations",
        "charges",
        "rate_lines",
        "extraction",
        "commodity_codes",
        "nbp_rates",
        "dangerous_goods",
        "networks",
        "channel_quotes",
    ):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "from app.models.credit_review" not in text
            assert "from app.domain.credit_review" not in text
            assert "from app.services.parties" not in text
            assert "CreditReview" not in text


def test_generated_api_types_include_credit_review() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CreditReviewResponse" in source
    assert "CreditReviewCreate" in source
