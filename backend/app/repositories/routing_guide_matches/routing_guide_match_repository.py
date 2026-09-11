from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.routing_guide_match import RoutingGuideMatch


class RoutingGuideMatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RoutingGuideMatch]:
        packed = await self._session.scalars(
            select(RoutingGuideMatch).order_by(
                RoutingGuideMatch.mark_code, RoutingGuideMatch.id
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: RoutingGuideMatch) -> RoutingGuideMatch:
        self._session.add(row)
        await self._session.flush()
        return row
