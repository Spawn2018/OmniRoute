from datetime import date
from uuid import UUID

from sqlalchemy import Date as SqlDate
from sqlalchemy import String, bindparam, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_calendar import OrganizationCalendar

# ISODOW 1=pn … 7=nd; default poniedziałek–piątek. HC-11: nie weekday() w Pythonie.
_WORKING_DAY_SQL = """
SELECT CASE
  WHEN ov.day_kind = 'holiday' THEN false
  WHEN ov.day_kind = 'working' THEN true
  ELSE EXTRACT(ISODOW FROM CAST(:calendar_day AS date)) < 6
END
FROM (SELECT CAST(:calendar_day AS date) AS asked) AS q
LEFT JOIN LATERAL (
  SELECT day_kind
  FROM organization_calendar
  WHERE country_code = :country_code
    AND calendar_day = CAST(:calendar_day AS date)
    AND superseded_by IS NULL
  ORDER BY created_at DESC, id
  LIMIT 1
) ov ON true
"""


class OrganizationCalendarRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current_for_country(self, country_code: str) -> list[OrganizationCalendar]:
        result = await self._session.scalars(
            select(OrganizationCalendar)
            .where(
                OrganizationCalendar.country_code == country_code,
                OrganizationCalendar.superseded_by.is_(None),
            )
            .order_by(OrganizationCalendar.calendar_day, OrganizationCalendar.id),
        )
        return list(result.all())

    async def find_current(
        self,
        country_code: str,
        calendar_day: date,
    ) -> OrganizationCalendar | None:
        result = await self._session.scalars(
            select(OrganizationCalendar)
            .where(
                OrganizationCalendar.country_code == country_code,
                OrganizationCalendar.calendar_day == calendar_day,
                OrganizationCalendar.superseded_by.is_(None),
            )
            .order_by(OrganizationCalendar.created_at.desc(), OrganizationCalendar.id),
        )
        return result.first()

    async def is_working_day(self, country_code: str, calendar_day: date) -> bool:
        stmt = text(_WORKING_DAY_SQL).bindparams(
            bindparam("country_code", type_=String),
            bindparam("calendar_day", type_=SqlDate),
        )
        flagged = await self._session.scalar(
            stmt,
            {"country_code": country_code, "calendar_day": calendar_day},
        )
        if type(flagged) is not bool:
            raise RuntimeError("is_working_day SQL nie zwróciło boolean")
        return flagged

    async def add(self, row: OrganizationCalendar) -> OrganizationCalendar:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(
        self,
        current: OrganizationCalendar,
        successor_id: UUID,
    ) -> OrganizationCalendar:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
