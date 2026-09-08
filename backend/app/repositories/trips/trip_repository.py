from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import Trip


class TripRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_current(self, status: str | None) -> list[Trip]:
        stmt = select(Trip).where(Trip.superseded_by.is_(None))
        if status is not None:
            stmt = stmt.where(Trip.status == status)
        result = await self._session.scalars(
            stmt.order_by(Trip.trip_no, Trip.id),
        )
        return list(result.all())

    async def find_current(self, trip_no: str) -> Trip | None:
        result = await self._session.scalars(
            select(Trip).where(
                Trip.trip_no == trip_no,
                Trip.superseded_by.is_(None),
            ),
        )
        found = list(result.all())
        return found[0] if found else None

    async def add(self, row: Trip) -> Trip:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: Trip, successor_id: UUID) -> Trip:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
