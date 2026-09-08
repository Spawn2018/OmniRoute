from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.organization_calendar import (
    require_calendar_day,
    require_calendar_source_ref,
    require_country_code,
    require_day_kind,
)
from app.models.organization_calendar import OrganizationCalendar
from app.repositories.organization_calendars.organization_calendar_repository import (
    OrganizationCalendarRepository,
)


class OrganizationCalendarService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OrganizationCalendarRepository(session)

    async def list_for_country(self, *, country_code: object) -> list[OrganizationCalendar]:
        return await self._rows.list_current_for_country(require_country_code(country_code))

    async def is_working_day(self, *, country_code: object, calendar_day: object) -> bool:
        return await self._rows.is_working_day(
            require_country_code(country_code),
            require_calendar_day(calendar_day),
        )

    async def record_day(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        country_code: object,
        calendar_day: object,
        day_kind: object,
        source_ref: object,
    ) -> OrganizationCalendar:
        code = require_country_code(country_code)
        day = require_calendar_day(calendar_day)
        kind = require_day_kind(day_kind)
        origin = require_calendar_source_ref(source_ref)
        current = await self._rows.find_current(code, day)
        if (
            current is not None
            and current.day_kind == kind
            and current.source_ref == origin
        ):
            return current
        saved = await self._rows.add(
            OrganizationCalendar(
                id=uuid4(),
                organization_id=organization_id,
                country_code=code,
                calendar_day=day,
                day_kind=kind,
                source_ref=origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
