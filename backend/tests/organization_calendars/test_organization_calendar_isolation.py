from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from app.core.database import bind_tenant
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
