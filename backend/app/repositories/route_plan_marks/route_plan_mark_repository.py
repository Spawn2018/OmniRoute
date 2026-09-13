from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.route_plan_mark import RoutePlanMark


class RoutePlanMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RoutePlanMark]:
        packed = await self._session.scalars(
            select(RoutePlanMark).order_by(RoutePlanMark.mark_code, RoutePlanMark.id),
        )
        return list(packed.all())

    async def add_mark(self, row: RoutePlanMark) -> RoutePlanMark:
        self._session.add(row)
        await self._session.flush()
        return row
