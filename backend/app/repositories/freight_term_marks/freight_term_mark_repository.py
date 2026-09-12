from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.freight_term_mark import FreightTermMark


def _freight_term_catalog_query() -> Select[tuple[FreightTermMark]]:
    return select(FreightTermMark).order_by(
        FreightTermMark.mark_code.asc(),
        FreightTermMark.created_at.desc(),
    )


class FreightTermMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FreightTermMark]:
        loaded = await self._session.scalars(_freight_term_catalog_query())
        batch: Sequence[FreightTermMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: FreightTermMark) -> FreightTermMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
