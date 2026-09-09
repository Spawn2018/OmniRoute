from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "126_kreptd_licence.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_126_creates_kreptd_licence_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "126_kreptd_licence"' in source
    assert 'down_revision: str | None = "125_lane_pattern"' in source
    assert '"kreptd_licence"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "kreptd_licence_tenant_isolation" in source
    assert "ix_kreptd_licence_org_licence" in source
    assert "uq_kreptd_licence_org_party" in source
    assert "buy_amount" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_kreptd_licence_service_does_not_import_parents() -> None:
    service = (_SERVICES / "kreptd_licences" / "kreptd_licence_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.parties" not in service
    assert "app.services.tenders" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.quotations" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_kreptd_licences_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.kreptd_licences" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.kreptd_licences" in forbidden
    assert "app.models.kreptd_licence" in forbidden


def test_generated_api_types_include_kreptd_licence() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "KreptdLicenceResponse" in source
    assert "KreptdLicenceCreate" in source
