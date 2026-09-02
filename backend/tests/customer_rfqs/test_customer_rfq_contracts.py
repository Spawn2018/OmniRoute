from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "028_customer_rfq_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_028_creates_customer_rfq_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "028_customer_rfq_rls"' in source
    assert 'down_revision: str | None = "027_inbound_message_party"' in source
    assert '"customer_rfq"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "customer_rfq_tenant_isolation" in source
    assert "uq_inbound_message_org_id" in source
    assert "uq_customer_rfq_org_message" in source
    assert "fk_customer_rfq_inbound_message" in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_rfq_service_does_not_import_inbound_or_quotations() -> None:
    service = (_SERVICES / "customer_rfqs" / "customer_rfq_service.py").read_text(encoding="utf-8")
    assert "app.services.inbound_messages" not in service
    assert "app.models.inbound_message" not in service
    assert "app.services.quotations" not in service
    assert "app.models.quotation" not in service
    assert "rate_line" not in service
    assert "amount" not in service


def test_importlinter_lists_customer_rfqs_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.customer_rfqs" in independence


def test_generated_api_types_include_customer_rfq() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "CustomerRfqResponse" in source or "CustomerRfqCreate" in source


def test_inbound_extract_api_does_not_create_rfq() -> None:
    source = (_ROOT / "backend" / "app" / "api" / "inbound_messages.py").read_text(
        encoding="utf-8",
    )
    assert "CustomerRfqService" not in source
    assert "customer_rfq" not in source
