from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diversion_mark import DiversionMark


def _diversion_catalog_query() -> Select[tuple[DiversionMark]]:
    return select(DiversionMark).order_by(
        DiversionMark.mark_code.asc(),
        DiversionMark.created_at.desc(),
    )


class DiversionMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DiversionMark]:
        loaded = await self._session.scalars(_diversion_catalog_query())
        batch: Sequence[DiversionMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: DiversionMark) -> DiversionMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
