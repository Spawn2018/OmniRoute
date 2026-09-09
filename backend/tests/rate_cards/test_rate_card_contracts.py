from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "103_rate_card.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_103_creates_rate_card_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "103_rate_card"' in source
    assert 'down_revision: str | None = "102_document_template"' in source
    assert '"rate_card"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "rate_card_tenant_isolation" in source
    assert "ix_rate_card_org_code" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_rate_card_service_does_not_import_parents() -> None:
    service = (_SERVICES / "rate_cards" / "rate_card_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.port_surcharges" not in service
    assert "app.services.rate_lines" not in service
    assert "app.services.charges" not in service
    assert "app.services.groupage_tariffs" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_rate_cards_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.rate_cards" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.rate_cards" in forbidden
    assert "app.models.rate_card" in forbidden


def test_generated_api_types_include_rate_card() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "RateCardResponse" in source
    assert "RateCardCreate" in source


def test_migration_145_indexes_applies_when_equality() -> None:
    source = (_ROOT / "backend" / "alembic" / "versions" / "145_rate_card_match.py").read_text(
        encoding="utf-8",
    )
    assert 'revision: str = "145_rate_card_match"' in source
    assert 'down_revision: str | None = "144_shipment_ref"' in source
    assert "ix_rate_card_org_when" in source
    assert "httpx" not in source
    assert "ast" not in source
    assert "def downgrade" in source
