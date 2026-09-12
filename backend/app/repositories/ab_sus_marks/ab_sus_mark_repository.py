from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ab_sus_mark import AbSusMark


def _label_parking_catalog_query() -> Select[tuple[AbSusMark]]:
    return select(AbSusMark).order_by(
        AbSusMark.mark_code.asc(),
        AbSusMark.created_at.desc(),
    )

class AbSusMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AbSusMark]:
        loaded = await self._session.scalars(_label_parking_catalog_query())
        batch: Sequence[AbSusMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: AbSusMark) -> AbSusMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
