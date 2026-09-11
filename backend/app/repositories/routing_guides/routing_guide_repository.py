
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.routing_guide import RoutingGuide


class RoutingGuideRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_guides(self) -> list[RoutingGuide]:
        packed = await self._session.scalars(
            select(RoutingGuide).order_by(RoutingGuide.guide_code, RoutingGuide.id),
        )
        return list(packed.all())

    async def add_guide(self, row: RoutingGuide) -> RoutingGuide:
        self._session.add(row)
        await self._session.flush()
        return row
