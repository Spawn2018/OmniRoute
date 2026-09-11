from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.routing_guide_enforcement import RoutingGuideEnforcement


class RoutingGuideEnforcementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RoutingGuideEnforcement]:
        packed = await self._session.scalars(
            select(RoutingGuideEnforcement).order_by(
                RoutingGuideEnforcement.mark_code, RoutingGuideEnforcement.id
            ),
        )
        return list(packed.all())

    async def add_mark(
        self, row: RoutingGuideEnforcement
    ) -> RoutingGuideEnforcement:
        self._session.add(row)
        await self._session.flush()
        return row
