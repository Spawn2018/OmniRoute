from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "095_groupage_line.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_095_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "095_groupage_line"' in source
    assert 'down_revision: str | None = "094_shipment_leg_air_kind"' in source
    assert '"groupage_line"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "groupage_line_tenant_isolation" in source
    assert "ix_groupage_line_org_code" in source
    assert "fk_groupage_line_origin" in source
    assert "buy_amount" not in source
    assert "wms_id" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_geography_or_quotes() -> None:
    service = (_SERVICES / "groupage_lines" / "groupage_line_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.geography" not in service
    assert "app.services.channel_quotes" not in service
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "httpx" not in service


def test_importlinter_lists_groupage_lines_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.groupage_lines" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.groupage_lines" in forbidden
    assert "app.models.groupage_line" in forbidden


def test_generated_api_types_include_groupage_line() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "GroupageLineResponse" in source
    assert "GroupageLineCreate" in source
