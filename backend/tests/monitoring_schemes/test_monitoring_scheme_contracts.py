from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "127_monitoring_scheme.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_127_creates_monitoring_scheme_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "127_monitoring_scheme"' in source
    assert 'down_revision: str | None = "126_kreptd_licence"' in source
    assert '"monitoring_scheme"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "monitoring_scheme_tenant_isolation" in source
    assert "uq_monitoring_scheme_org_code" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_monitoring_scheme_service_does_not_import_parents() -> None:
    service = (_SERVICES / "monitoring_schemes" / "monitoring_scheme_service.py").read_text(
        encoding="utf-8"
    )
    assert "app.services.shipments" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_monitoring_schemes_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.monitoring_schemes" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.monitoring_schemes" in forbidden
    assert "app.models.monitoring_scheme" in forbidden


def test_generated_api_types_include_monitoring_scheme() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "MonitoringSchemeResponse" in source
    assert "MonitoringSchemeCreate" in source
