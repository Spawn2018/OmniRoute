from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "376_factoring_connector.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_376_creates_factoring_connector_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "376_factoring_connector"' in source
    assert 'down_revision: str | None = "375_silk_corridor_mark"' in source
    assert '"factoring_connector"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "factoring_connector_tenant_isolation" in source
    assert "uq_factoring_connector_org_source_ref" in source
    assert "uq_factoring_connector_org_code" in source
    assert "smeo" in source
    assert "buy_amount" not in source
    assert "credential" not in source
    assert "ciphertext" not in source
    assert "base_url" not in source
    assert "httpx" not in source
    assert "float(" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_factoring_connector_service_is_catalog_and_isolated() -> None:
    service = (
        _SERVICES / "factoring_connectors" / "factoring_connector_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.charges" not in service
    assert "app.services.sales_invoices" not in service
    assert "app.services.bank_payments" not in service
    assert "app.services.working_capital_marks" not in service
    assert "httpx" not in service
    assert "float(" not in service
    assert "UPDATE" not in service
    assert "DELETE" not in service
    assert "delete(" not in service
    assert ".update(" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_factoring_connectors_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.factoring_connectors" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.factoring_connectors" in forbidden
    assert "app.models.factoring_connector" in forbidden
