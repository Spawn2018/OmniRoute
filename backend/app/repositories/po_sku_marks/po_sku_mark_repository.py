from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.po_sku_mark import PoSkuMark


def _po_sku_catalog_query() -> Select[tuple[PoSkuMark]]:
    return select(PoSkuMark).order_by(
        PoSkuMark.mark_code.asc(),
        PoSkuMark.created_at.desc(),
    )


class PoSkuMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PoSkuMark]:
        loaded = await self._session.scalars(_po_sku_catalog_query())
        batch: Sequence[PoSkuMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: PoSkuMark) -> PoSkuMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
