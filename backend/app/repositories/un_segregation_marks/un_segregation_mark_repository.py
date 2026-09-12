from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.un_segregation_mark import UnSegregationMark


def _un_segregation_catalog_query() -> Select[tuple[UnSegregationMark]]:
    return select(UnSegregationMark).order_by(
        UnSegregationMark.mark_code.asc(),
        UnSegregationMark.created_at.desc(),
    )


class UnSegregationMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[UnSegregationMark]:
        loaded = await self._session.scalars(_un_segregation_catalog_query())
        batch: Sequence[UnSegregationMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: UnSegregationMark) -> UnSegregationMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
