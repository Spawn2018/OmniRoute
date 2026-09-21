from datetime import date, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
from app.domain.errors import InvalidOrganizationCalendar, InvalidOrganizationSetting
from app.models.organization_calendar import OrganizationCalendar
from app.services.organization_calendars.organization_calendar_service import (
    OrganizationCalendarService,
)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_organization_calendar_rls_isolates_tenants(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    user_b = two_tenants["user_b"]

    await bind_tenant(session, org_a.id)
    row_a = OrganizationCalendar(
        id=uuid4(),
        organization_id=org_a.id,
        country_code="PL",
        calendar_day=date(2026, 9, 4),
        day_kind="holiday",
        source_ref="fixture://organization-calendar/a",
        created_by=user_a.id,
    )
    session.add(row_a)
    await session.flush()

    await bind_tenant(session, org_b.id)
    row_b = OrganizationCalendar(
        id=uuid4(),
        organization_id=org_b.id,
        country_code="DE",
        calendar_day=date(2026, 9, 5),
        day_kind="working",
        source_ref="fixture://organization-calendar/b",
        created_by=user_b.id,
    )
    session.add(row_b)
    await session.flush()

    session.expunge_all()
    await bind_tenant(session, org_a.id)
    visible_a = list((await session.scalars(select(OrganizationCalendar))).all())
    assert {row.id for row in visible_a} == {row_a.id}
    assert await session.scalar(
        select(OrganizationCalendar).where(OrganizationCalendar.id == row_b.id),
    ) is None

    session.expunge_all()
    await bind_tenant(session, org_b.id)
    visible_b = list((await session.scalars(select(OrganizationCalendar))).all())
    assert {row.id for row in visible_b} == {row_b.id}


@pytest.mark.integration
@pytest.mark.asyncio
async def test_organization_calendar_list_uses_org_country_day_index(
    session,
    two_tenants,
) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT id FROM organization_calendar "
            "WHERE organization_id = :org_id AND country_code = 'PL' "
            "AND calendar_day = DATE '2026-09-04' AND superseded_by IS NULL"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "ix_organization_calendar_org_country_day" in joined


@pytest.mark.integration
@pytest.mark.asyncio
async def test_is_working_day_sql_default_and_overrides(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    service = OrganizationCalendarService(session)
    monday = date(2026, 9, 7)
    sunday = date(2026, 9, 6)
    friday = date(2026, 9, 4)
    assert await service.is_working_day(country_code="PL", calendar_day=monday) is True
    assert await service.is_working_day(country_code="PL", calendar_day=sunday) is False
    await service.record_day(
        organization_id=org_a.id,
        user_id=user_a.id,
        country_code="PL",
        calendar_day=friday,
        day_kind="holiday",
        source_ref="fixture://organization-calendar/holiday",
    )
    assert await service.is_working_day(country_code="PL", calendar_day=friday) is False
    await service.record_day(
        organization_id=org_a.id,
        user_id=user_a.id,
        country_code="PL",
        calendar_day=sunday,
        day_kind="working",
        source_ref="fixture://organization-calendar/sunday",
    )
    assert await service.is_working_day(country_code="PL", calendar_day=sunday) is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fx_rate_day_sql_is_previous_working_day(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    org_b = two_tenants["org_b"]
    user_a = two_tenants["user_a"]
    monday = date(2026, 9, 7)
    friday = date(2026, 9, 4)
    thursday = date(2026, 9, 3)
    sunday = date(2026, 9, 6)

    await bind_tenant(session, org_a.id)
    service_a = OrganizationCalendarService(session)
    assert await service_a.fx_rate_day(
        country_code="PL",
        anchor=sunday,
        offset_days="-1",
    ) == friday
    assert await service_a.fx_rate_day(
        country_code="PL",
        anchor=sunday,
        offset_days="0",
    ) == sunday
    await service_a.record_day(
        organization_id=org_a.id,
        user_id=user_a.id,
        country_code="PL",
        calendar_day=friday,
        day_kind="holiday",
        source_ref="fixture://organization-calendar/fx-holiday",
    )
    assert await service_a.fx_rate_day(
        country_code="PL",
        anchor=monday,
        offset_days="-1",
    ) == thursday

    await bind_tenant(session, org_b.id)
    service_b = OrganizationCalendarService(session)
    assert await service_b.fx_rate_day(
        country_code="PL",
        anchor=monday,
        offset_days="-1",
    ) == friday
    with pytest.raises(InvalidOrganizationSetting, match="dni"):
        await service_b.fx_rate_day(country_code="PL", anchor=monday, offset_days="2")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fx_rate_day_rejects_full_holiday_window(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    user_a = two_tenants["user_a"]
    await bind_tenant(session, org_a.id)
    service = OrganizationCalendarService(session)
    anchor = date(2026, 9, 7)
    for step in range(1, 15):
        await service.record_day(
            organization_id=org_a.id,
            user_id=user_a.id,
            country_code="PL",
            calendar_day=anchor - timedelta(days=step),
            day_kind="holiday",
            source_ref=f"fixture://organization-calendar/fx-gap-{step}",
        )
    with pytest.raises(InvalidOrganizationCalendar, match="dni"):
        await service.fx_rate_day(country_code="PL", anchor=anchor, offset_days="-1")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_fx_rate_day_explain_reads_calendar(session, two_tenants) -> None:
    org_a = two_tenants["org_a"]
    await bind_tenant(session, org_a.id)
    plan = await session.execute(
        text(
            "EXPLAIN SELECT MAX(c.candidate) "
            "FROM generate_series(1, 14) AS gs(day_back) "
            "CROSS JOIN LATERAL ("
            "SELECT (DATE '2026-09-07' - gs.day_back) AS candidate"
            ") AS c "
            "LEFT JOIN LATERAL ("
            "SELECT day_kind FROM organization_calendar "
            "WHERE organization_id = :org_id AND country_code = 'PL' "
            "AND calendar_day = c.candidate AND superseded_by IS NULL "
            "ORDER BY created_at DESC, id LIMIT 1"
            ") ov ON true"
        ),
        {"org_id": org_a.id},
    )
    joined = " ".join(str(row[0]) for row in plan)
    assert "organization_calendar" in joined
    assert "ix_organization_calendar_org_country_day" in joined
