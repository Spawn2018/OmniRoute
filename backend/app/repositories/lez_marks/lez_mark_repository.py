from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lez_mark import LezMark


def _lez_catalog_query() -> Select[tuple[LezMark]]:
    return select(LezMark).order_by(
        LezMark.mark_code.asc(),
        LezMark.created_at.desc(),
    )


class LezMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LezMark]:
        loaded = await self._session.scalars(_lez_catalog_query())
        batch: Sequence[LezMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: LezMark) -> LezMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
