from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "035_operator_notice_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_035_creates_operator_notice_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "035_operator_notice_rls"' in source
    assert 'down_revision: str | None = "034_operator_decision_rls"' in source
    assert '"operator_notice"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "operator_notice_tenant_isolation" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_notice_service_does_not_import_quotes_or_extract() -> None:
    service = (_SERVICES / "operator_notices" / "operator_notice_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.quotations" not in service
    assert "app.models.quotation" not in service
    assert "app.services.extraction" not in service
    assert "app.services.inbound_messages" not in service
    assert "rate_line" not in service
    assert "amount" not in service


def test_importlinter_lists_operator_notices_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.operator_notices" in independence


def test_generated_api_types_include_operator_notice() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OperatorNoticeResponse" in source or "OperatorNoticeCreate" in source
