from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.csrd_mark import CsrdMark


def _csrd_catalog_query() -> Select[tuple[CsrdMark]]:
    return select(CsrdMark).order_by(CsrdMark.mark_code.asc(), CsrdMark.created_at.desc())


class CsrdMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CsrdMark]:
        loaded = await self._session.scalars(_csrd_catalog_query())
        batch: Sequence[CsrdMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: CsrdMark) -> CsrdMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
