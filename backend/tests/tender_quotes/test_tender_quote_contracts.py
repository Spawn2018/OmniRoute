from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "108_tender_quote.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_108_creates_tender_quote_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "108_tender_quote"' in source
    assert 'down_revision: str | None = "107_trip_expected_buy"' in source
    assert '"tender_quote"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "tender_quote_tenant_isolation" in source
    assert "ix_tender_quote_org_quotation" in source
    assert "buy_amount" not in source
    assert "tender_lot" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_tender_quote_service_does_not_import_parents() -> None:
    service = (_SERVICES / "tender_quotes" / "tender_quote_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.quotations" not in service
    assert "app.services.charges" not in service
    assert "app.services.channel_quotes" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_tender_quotes_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.tender_quotes" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.tender_quotes" in forbidden
    assert "app.models.tender_quote" in forbidden


def test_generated_api_types_include_tender_quote() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "TenderQuoteResponse" in source
    assert "TenderQuoteCreate" in source
