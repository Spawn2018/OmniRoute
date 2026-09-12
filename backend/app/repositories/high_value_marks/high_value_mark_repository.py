from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.high_value_mark import HighValueMark


def _high_value_catalog_query() -> Select[tuple[HighValueMark]]:
    return select(HighValueMark).order_by(
        HighValueMark.mark_code.asc(),
        HighValueMark.created_at.desc(),
    )


class HighValueMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[HighValueMark]:
        loaded = await self._session.scalars(_high_value_catalog_query())
        batch: Sequence[HighValueMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: HighValueMark) -> HighValueMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
