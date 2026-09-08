from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
_MIGRATION = _ROOT / "backend" / "alembic" / "versions" / "089_organization_calendar.py"
_SERVICES = _ROOT / "backend" / "app" / "services"
_REPO = (
    _ROOT
    / "backend"
    / "app"
    / "repositories"
    / "organization_calendars"
    / "organization_calendar_repository.py"
)


def test_migration_089_creates_table_and_forces_rls() -> None:
    source = _MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "089_organization_calendar"' in source
    assert 'down_revision: str | None = "088_booking_instruction"' in source
    assert '"organization_calendar"' in source
    assert "FORCE ROW LEVEL SECURITY" in source
    assert "organization_calendar_tenant_isolation" in source
    assert "ix_organization_calendar_org_country_day" in source
    assert "buy_amount" not in source
    assert "observation_ends_at" not in source
    assert "httpx" not in source
    assert "def downgrade" in source
    assert "drop_table" in source.split("def downgrade")[1]


def test_service_does_not_import_parents_or_count_weekdays() -> None:
    service = (
        _SERVICES / "organization_calendars" / "organization_calendar_service.py"
    ).read_text(encoding="utf-8")
    assert "app.services.parties" not in service
    assert "app.services.shipments" not in service
    assert "app.services.charges" not in service
    assert "app.services.nbp_rates" not in service
    assert "isoweekday" not in service
    assert "weekday(" not in service
    assert "httpx" not in service
    assert "buy_amount" not in service


def test_working_day_query_is_sql_not_python() -> None:
    source = _REPO.read_text(encoding="utf-8")
    assert "EXTRACT(ISODOW" in source
    assert "isoweekday" not in source
    assert "timedelta" not in source
    assert "calendar.weekday" not in source


def test_importlinter_lists_organization_calendars_as_independent() -> None:
    source = (_ROOT / ".importlinter").read_text(encoding="utf-8")
    independence = source.split("[importlinter:contract:moduly]", 1)[1].split(
        "[importlinter:",
        1,
    )[0]
    assert "app.services.organization_calendars" in independence
    forbidden = source.split("[importlinter:contract:extraction-no-rates]", 1)[1]
    assert "app.services.organization_calendars" in forbidden
    assert "app.models.organization_calendar" in forbidden


def test_generated_api_types_include_organization_calendar() -> None:
    source = (_ROOT / "frontend" / "src" / "api" / "types.gen.ts").read_text(encoding="utf-8")
    assert "OrganizationCalendarResponse" in source
    assert "OrganizationCalendarCreate" in source
    assert "WorkingDayResponse" in source
