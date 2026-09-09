from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "136_free_time_clock.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_136_creates_free_time_clock_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "136_free_time_clock"' in source
    assert 'down_revision: str | None = "135_weather_observation"' in source
    assert '"free_time_clock"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "free_time_clock_tenant_isolation" in source
    assert "uq_free_time_clock_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_free_time_clock_service_does_not_import_parents() -> None:
    service = (_SERVICES / "free_time_clocks" / "free_time_clock_service.py").read_text(
        encoding="utf-8",
    )
    assert "app.services.containers" not in service
    assert "app.services.charges" not in service
    assert "app.services.extraction" not in service
    assert "app.services.trips" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service
    assert "timedelta" not in service


def test_importlinter_lists_free_time_clocks_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.free_time_clocks" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.free_time_clocks" in forbidden
    assert "app.models.free_time_clock" in forbidden


def test_generated_api_types_include_free_time_clock() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "FreeTimeClockResponse" in source
    assert "FreeTimeClockCreate" in source
