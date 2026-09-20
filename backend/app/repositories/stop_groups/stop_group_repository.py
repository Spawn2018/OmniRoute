from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stop_group import StopGroup


class StopGroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[StopGroup]:
        result = await self._session.scalars(
            select(StopGroup).order_by(
                StopGroup.created_at.desc(),
                StopGroup.id,
            ),
        )
        return list(result.all())

    async def get_by_id(self, group_id: object) -> StopGroup | None:
        loaded = await self._session.scalar(
            select(StopGroup).where(StopGroup.id == group_id).limit(1),
        )
        if loaded is None:
            return None
        return loaded

    async def add(self, row: StopGroup) -> StopGroup:
        self._session.add(row)
        await self._session.flush()
        return row
