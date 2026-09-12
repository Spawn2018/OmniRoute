from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.e_doreczenia_mark import EDoreczeniaMark


def _e_doreczenia_catalog_query() -> Select[tuple[EDoreczeniaMark]]:
    return select(EDoreczeniaMark).order_by(
        EDoreczeniaMark.mark_code.asc(),
        EDoreczeniaMark.created_at.desc(),
    )


class EDoreczeniaMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[EDoreczeniaMark]:
        loaded = await self._session.scalars(_e_doreczenia_catalog_query())
        batch: Sequence[EDoreczeniaMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: EDoreczeniaMark) -> EDoreczeniaMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
