from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "034_operator_decision_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_034_creates_operator_decision_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "034_operator_decision_rls"' in source
    assert 'down_revision: str | None = "033_customer_sop_blocks_auto"' in source
    assert '"operator_decision"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "operator_decision_tenant_isolation" in source
    assert "uq_operator_decision_pending" in source
    assert "status = 'pending'" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_decision_service_does_not_import_inbound_or_extract() -> None:
    service = (_SERVICES / "operator_decisions" / "operator_decision_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.inbound_messages" not in service
    assert "app.models.inbound_message" not in service
    assert "app.services.quotations" not in service
    assert "app.models.quotation" not in service
    assert "app.services.extraction" not in service
    assert "rate_line" not in service
    assert "amount" not in service


def test_importlinter_lists_operator_decisions_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.operator_decisions" in independence


def test_generated_api_types_include_operator_decision() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OperatorDecisionResponse" in source or "OperatorDecisionCreate" in source


def test_migration_045_allows_quotation_subject() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "045_operator_decision_quotation.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "045_operator_decision_quotation"' in source
    assert "044_quotation_negotiated_channel" in source
    assert "quotation" in source
    assert "won" not in source
    assert "amount" not in source


def test_migration_037_adds_lock_version() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "037_operator_decision_lock.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "037_operator_decision_lock"' in source
    assert "lock_version" in source
    assert "036_mail_draft_rls" in source
