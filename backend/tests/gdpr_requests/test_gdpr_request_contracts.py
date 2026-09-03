from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "064_gdpr_request_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_064_creates_gdpr_request_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "064_gdpr_request_rls"' in source
    assert 'down_revision: str | None = "063_collective_invoice_rls"' in source
    assert '"gdpr_request"' in source
    assert "uq_app_user_org_id" in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "gdpr_request_tenant_isolation" in source
    assert "fk_gdpr_request_app_user" in source
    assert "uq_gdpr_request_open" in source
    assert "buy_amount" not in source
    assert "password_hash" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_gdpr_request_service_does_not_import_tenancy() -> None:
    service = (_SERVICES / "gdpr_requests" / "gdpr_request_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.tenancy" not in service
    assert "httpx" not in service
    assert "password_hash" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_gdpr_request_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.gdpr_requests" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.gdpr_requests" in forbidden
    assert "app.models.gdpr_request" in forbidden


def test_generated_api_types_include_gdpr_request() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "GdprRequestResponse" in source
    assert "GdprRequestCreate" in source
