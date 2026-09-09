from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "128_party_document.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_128_creates_party_document_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "128_party_document"' in source
    assert 'down_revision: str | None = "127_monitoring_scheme"' in source
    assert '"party_document"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "party_document_tenant_isolation" in source
    assert "uq_party_document_org_party_kind" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_party_document_service_does_not_import_parents() -> None:
    service = (_SERVICES / "party_documents" / "party_document_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.parties" not in service
    assert "app.services.shipments" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_party_documents_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.party_documents" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.party_documents" in forbidden
    assert "app.models.party_document" in forbidden


def test_generated_api_types_include_party_document() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "PartyDocumentResponse" in source
    assert "PartyDocumentCreate" in source
