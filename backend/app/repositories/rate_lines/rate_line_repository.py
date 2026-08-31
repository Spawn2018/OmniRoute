from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rate_line import RateLine


class RateLineRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[RateLine]:
        result = await self._session.scalars(
            select(RateLine).order_by(RateLine.created_at.desc(), RateLine.id),
        )
        return list(result.all())

    async def get(self, rate_line_id: UUID) -> RateLine | None:
        found = await self._session.get(RateLine, rate_line_id)
        return found if isinstance(found, RateLine) else None

    async def add(self, row: RateLine) -> RateLine:
        self._session.add(row)
        await self._session.flush()
        return row

    async def mark_superseded(self, current: RateLine, successor_id: UUID) -> RateLine:
        current.superseded_by = successor_id
        await self._session.flush()
        return current
