from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "023_port_surcharge_rls.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_023_creates_port_surcharge_and_forces_rls() -> None:
    assert _MIGRATION.is_file()
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "023_port_surcharge_rls"' in source
    assert 'down_revision: str | None = "022_customer_sop_rls"' in source
    assert '"port_surcharge"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "port_surcharge_tenant_isolation" in source
    assert "source_ref" in source
    lowered = source.lower()
    assert "numeric(14, 4)" in lowered or "numeric(14,4)" in lowered
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_importlinter_lists_port_surcharges_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.port_surcharges" in independence


def test_pricing_and_extraction_do_not_import_port_surcharges() -> None:
    for bounded in ("quotations", "charges", "rate_lines", "extraction", "parties"):
        for path in (_SERVICES / bounded).rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "port_surcharge" not in text
            assert "PortSurcharge" not in text
            assert "app.services.port_surcharges" not in text


def test_generated_api_types_include_port_surcharge() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "PortSurchargeResponse" in source
    assert "PortSurchargeCreate" in source
