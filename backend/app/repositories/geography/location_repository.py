from uuid import UUID

from sqlalchemy import String, bindparam, func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location, LocationZoneMember

# Typ postal_range z kolacją "C" nie ma odpowiednika w ORM, a literał bez rzutowania
# Postgres parsuje jako zakres, nie element.
_CODE_IN_SPAN = text("location_zone_member.postal_span @> cast(:postal_code as text)")


class LocationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(
        self,
        *,
        kind: str | None = None,
        search: str | None = None,
    ) -> list[Location]:
        stmt = select(Location).order_by(Location.kind, Location.name)
        if kind is not None:
            stmt = stmt.where(Location.kind == kind)
        token = "" if search is None else search.strip().upper()
        if token != "":
            pattern = f"%{token}%"
            stmt = stmt.where(
                or_(func.upper(Location.name).like(pattern), Location.code.like(pattern)),
            )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def get(self, location_id: UUID) -> Location | None:
        found = await self._session.get(Location, location_id)
        return found if isinstance(found, Location) else None

    async def find_by_code(self, code: str) -> Location | None:
        found = await self._session.scalar(select(Location).where(Location.code == code))
        return found if isinstance(found, Location) else None

    async def list_members(self, zone_id: UUID) -> list[LocationZoneMember]:
        stmt = (
            select(LocationZoneMember)
            .where(LocationZoneMember.zone_location_id == zone_id)
            .order_by(LocationZoneMember.country_code, LocationZoneMember.postal_from)
        )
        result = await self._session.scalars(stmt)
        return list(result.all())

    async def find_zone_by_postal(self, *, country_code: str, postal_code: str) -> Location | None:
        # Warunek długości jest niezbędny: bez niego 811989 wpada leksykograficznie
        # w zakres [81000, 81999].
        stmt = (
            select(Location)
            .join(LocationZoneMember, LocationZoneMember.zone_location_id == Location.id)
            .where(
                LocationZoneMember.country_code == country_code,
                func.length(LocationZoneMember.postal_from) == len(postal_code),
                _CODE_IN_SPAN.bindparams(
                    bindparam("postal_code", postal_code, type_=String),
                ),
            )
        )
        found = await self._session.scalar(stmt)
        return found if isinstance(found, Location) else None

    async def add_location(self, row: Location) -> Location:
        self._session.add(row)
        await self._session.flush()
        return row

    async def add_member(self, row: LocationZoneMember) -> LocationZoneMember:
        self._session.add(row)
        await self._session.flush()
        return row
