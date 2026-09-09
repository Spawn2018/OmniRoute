from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "135_weather_observation.py"
_SERVICES = _ROOT / "backend" / "app" / "services"


def test_migration_135_creates_weather_observation_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "135_weather_observation"' in source
    assert 'down_revision: str | None = "134_stop_eta"' in source
    assert '"weather_observation"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "weather_observation_tenant_isolation" in source
    assert "uq_weather_observation_org_source_ref" in source
    assert "buy_amount" not in source
    assert "Numeric" not in source
    assert "httpx" not in source
    assert "open-meteo" not in source.casefold()
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_weather_observation_service_does_not_import_parents() -> None:
    service = (
        _SERVICES / "weather_observations" / "weather_observation_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.trips" not in service
    assert "app.services.stops" not in service
    assert "app.services.extraction" not in service
    assert "app.services.charges" not in service
    assert "app.services.geography" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_importlinter_lists_weather_observations_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.weather_observations" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.weather_observations" in forbidden
    assert "app.models.weather_observation" in forbidden


def test_generated_api_types_include_weather_observation() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(
        encoding="utf-8",
    )
    assert "WeatherObservationResponse" in source
    assert "WeatherObservationCreate" in source
