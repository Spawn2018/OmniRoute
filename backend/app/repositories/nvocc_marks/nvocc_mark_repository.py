from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.nvocc_mark import NvoccMark


def _nvocc_catalog_query() -> Select[tuple[NvoccMark]]:
    return select(NvoccMark).order_by(
        NvoccMark.mark_code.asc(),
        NvoccMark.created_at.desc(),
    )


class NvoccMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[NvoccMark]:
        loaded = await self._session.scalars(_nvocc_catalog_query())
        batch: Sequence[NvoccMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: NvoccMark) -> NvoccMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
