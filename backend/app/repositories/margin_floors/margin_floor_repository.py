from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.margin_floor import MarginFloor


def _floor_query() -> Select[tuple[MarginFloor]]:
    return select(MarginFloor).order_by(
        MarginFloor.created_at.desc(),
        MarginFloor.id,
    )


class MarginFloorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[MarginFloor]:
        loaded = await self._session.scalars(_floor_query())
        batch: Sequence[MarginFloor] = loaded.all()
        return list(batch)

    async def add(self, entity: MarginFloor) -> MarginFloor:
        self._session.add(entity)
        await self._session.flush()
        return entity
