from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "099_groupage_tariff.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_099_creates_groupage_tariff_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "099_groupage_tariff"' in source
    assert 'down_revision: str | None = "098_cod_instruction"' in source
    assert '"groupage_tariff"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "groupage_tariff_tenant_isolation" in source
    assert "fk_groupage_tariff_location" in source
    assert "ix_groupage_tariff_org_location" in source
    assert "Numeric(14, 4)" in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_migration_497_adds_optional_volume() -> None:
    source = (
        _ROOT / "backend" / "alembic" / "versions" / "497_groupage_tariff_volume.py"
    ).read_text(encoding="utf-8")
    assert 'revision: str = "497_groupage_tariff_volume"' in source
    assert 'down_revision: str | None = "496_shipment_document_rod"' in source
    assert "volume_m3" in source
    assert "create_table" not in source
    assert "httpx" not in source


def test_groupage_tariff_service_does_not_import_parents() -> None:
    service = (_SERVICES / "groupage_tariffs" / "groupage_tariff_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.geography" not in service
    assert "app.services.charges" not in service
    assert "app.services.rate_lines" not in service
    assert "httpx" not in service
    assert "float(" not in service


def test_importlinter_lists_groupage_tariffs_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.groupage_tariffs" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.groupage_tariffs" in forbidden
    assert "app.models.groupage_tariff" in forbidden


def test_generated_api_types_include_groupage_tariff() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "GroupageTariffResponse" in source
    assert "GroupageTariffCreate" in source
