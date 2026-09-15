from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.impact_node_mark import ImpactNodeMark


class ImpactNodeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ImpactNodeMark]:
        packed = await self._session.scalars(
            select(ImpactNodeMark).order_by(
                ImpactNodeMark.mark_code,
                ImpactNodeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: ImpactNodeMark) -> ImpactNodeMark:
        self._session.add(row)
        await self._session.flush()
        return row
