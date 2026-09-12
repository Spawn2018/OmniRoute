from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.empty_depot_mark import EmptyDepotMark


def _depot_catalog_query() -> Select[tuple[EmptyDepotMark]]:
    return select(EmptyDepotMark).order_by(
        EmptyDepotMark.mark_code.asc(),
        EmptyDepotMark.created_at.desc(),
    )


class EmptyDepotMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[EmptyDepotMark]:
        loaded = await self._session.scalars(_depot_catalog_query())
        batch: Sequence[EmptyDepotMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: EmptyDepotMark) -> EmptyDepotMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
