from pathlib import Path

_MIGRATION = Path("backend/alembic/versions/014_terminal_rls.py")


def test_migration_014_creates_terminal_alters_port_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "014_terminal_rls"' in source
    assert 'down_revision: str | None = "013_location_rls"' in source
    assert "create_table" in source
    assert '"terminal"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "terminal_tenant_isolation" in source
    assert "WITH CHECK" in source
    assert "uq_terminal_org_isps" in source
    assert "uq_terminal_org_port_name" in source
    assert "fk_terminal_port" in source
    assert "wpi_number" in source
    assert "harbor_size" in source
    assert "harbor_type" in source
    assert "shelter" in source
    assert "channel_depth_m" in source
    assert "cargo_pier_depth_m" in source
    assert "wpi_source_ref" in source
    assert "ck_port_harbor_size" in source
    assert "ck_port_harbor_type" in source
    assert "ck_port_shelter" in source
    assert "def downgrade" in source
    assert "drop_table" in source and "terminal" in source
    assert "drop_column" in source or "wpi_number" in source.split("def downgrade")[1]


def test_conftest_registers_terminal_model_without_duplicating_rls() -> None:
    source = Path("backend/tests/conftest.py").read_text(encoding="utf-8")
    assert "from app.models.terminal import" in source
    assert "terminal_tenant_isolation" not in source


def test_generated_api_types_include_terminal_and_wpi_fields() -> None:
    source = Path("frontend/src/api/types.gen.ts").read_text(encoding="utf-8")
    assert "TerminalResponse" in source or "Terminal" in source
    assert "wpi_number" in source
    assert "isps_code" in source
