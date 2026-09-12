from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.funnel_mark import FunnelMark


def _label_parking_catalog_query() -> Select[tuple[FunnelMark]]:
    return select(FunnelMark).order_by(
        FunnelMark.mark_code.asc(),
        FunnelMark.created_at.desc(),
    )

class FunnelMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FunnelMark]:
        loaded = await self._session.scalars(_label_parking_catalog_query())
        batch: Sequence[FunnelMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: FunnelMark) -> FunnelMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
