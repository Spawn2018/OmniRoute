from datetime import date
from uuid import UUID

from sqlalchemy import Date as SqlDate
from sqlalchemy import String, bindparam, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization_calendar import OrganizationCalendar


# ISODOW 1=pn … 7=nd; default poniedziałek–piątek. HC-11: nie weekday() w Pythonie.
# NBP D-1 roboczy — art. 31a ustawy o VAT. Okno 14 dni zostaje w jednym SELECT.
def _working_case(day_sql: str) -> str:
    return (
        "CASE "
        "WHEN ov.day_kind = 'holiday' THEN false "
        "WHEN ov.day_kind = 'working' THEN true "
        f"ELSE EXTRACT(ISODOW FROM {day_sql}) < 6 END"
    )


def _override_join(day_sql: str) -> str:
    return (
        "LEFT JOIN LATERAL ("
        "SELECT day_kind FROM organization_calendar "
        "WHERE country_code = :country_code "
        f"AND calendar_day = {day_sql} "
        "AND superseded_by IS NULL "
        "ORDER BY created_at DESC, id LIMIT 1"
        ") ov ON true"
    )


_WORKING_DAY_SQL = (
    f"SELECT {_working_case('CAST(:calendar_day AS date)')} "
    "FROM (SELECT CAST(:calendar_day AS date) AS asked) AS q "
    f"{_override_join('CAST(:calendar_day AS date)')}"
)

_FX_RATE_DAY_SQL = (
    "SELECT CASE "
    "WHEN :offset_days = '0' THEN CAST(:anchor AS date) "
    "ELSE ("
    "SELECT MAX(c.candidate) FROM generate_series(1, 14) AS gs(day_back) "
    "CROSS JOIN LATERAL (SELECT (CAST(:anchor AS date) - gs.day_back) AS candidate) AS c "
    "WHERE ("
    f"SELECT {_working_case('c.candidate')} "
    "FROM (SELECT c.candidate AS asked) AS q "
    f"{_override_join('c.candidate')}"
    ")) END"
)


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

    async def fx_rate_day(
        self,
        country_code: str,
        anchor: date,
        offset_days: str,
    ) -> date | None:
        stmt = text(_FX_RATE_DAY_SQL).bindparams(
            bindparam("country_code", type_=String),
            bindparam("anchor", type_=SqlDate),
            bindparam("offset_days", type_=String),
        )
        resolved = await self._session.scalar(
            stmt,
            {
                "country_code": country_code,
                "anchor": anchor,
                "offset_days": offset_days,
            },
        )
        if resolved is None:
            return None
        if type(resolved) is not date:
            raise RuntimeError("fx_rate_day SQL nie zwróciło daty")
        return resolved

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
