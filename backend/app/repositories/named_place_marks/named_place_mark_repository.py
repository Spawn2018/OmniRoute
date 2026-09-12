from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.named_place_mark import NamedPlaceMark


def _named_place_catalog_query() -> Select[tuple[NamedPlaceMark]]:
    return select(NamedPlaceMark).order_by(
        NamedPlaceMark.mark_code.asc(),
        NamedPlaceMark.created_at.desc(),
    )


class NamedPlaceMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[NamedPlaceMark]:
        loaded = await self._session.scalars(_named_place_catalog_query())
        batch: Sequence[NamedPlaceMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: NamedPlaceMark) -> NamedPlaceMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
