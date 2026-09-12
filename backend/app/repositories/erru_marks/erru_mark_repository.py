from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.erru_mark import ErruMark


def _erru_catalog_query() -> Select[tuple[ErruMark]]:
    return select(ErruMark).order_by(
        ErruMark.mark_code.asc(),
        ErruMark.created_at.desc(),
    )


class ErruMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ErruMark]:
        loaded = await self._session.scalars(_erru_catalog_query())
        batch: Sequence[ErruMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ErruMark) -> ErruMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
