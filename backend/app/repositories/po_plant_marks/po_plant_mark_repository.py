from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.po_plant_mark import PoPlantMark


def _po_plant_catalog_query() -> Select[tuple[PoPlantMark]]:
    return select(PoPlantMark).order_by(
        PoPlantMark.mark_code.asc(),
        PoPlantMark.created_at.desc(),
    )


class PoPlantMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PoPlantMark]:
        loaded = await self._session.scalars(_po_plant_catalog_query())
        batch: Sequence[PoPlantMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: PoPlantMark) -> PoPlantMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
