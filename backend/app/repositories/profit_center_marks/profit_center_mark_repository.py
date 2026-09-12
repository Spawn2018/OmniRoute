from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profit_center_mark import ProfitCenterMark


def _profit_center_catalog_query() -> Select[tuple[ProfitCenterMark]]:
    return select(ProfitCenterMark).order_by(
        ProfitCenterMark.mark_code.asc(),
        ProfitCenterMark.created_at.desc(),
    )


class ProfitCenterMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ProfitCenterMark]:
        loaded = await self._session.scalars(_profit_center_catalog_query())
        batch: Sequence[ProfitCenterMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ProfitCenterMark) -> ProfitCenterMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
