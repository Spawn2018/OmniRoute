from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.po_batch_mark import PoBatchMark


def _po_batch_catalog_query() -> Select[tuple[PoBatchMark]]:
    return select(PoBatchMark).order_by(
        PoBatchMark.mark_code.asc(),
        PoBatchMark.created_at.desc(),
    )


class PoBatchMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PoBatchMark]:
        loaded = await self._session.scalars(_po_batch_catalog_query())
        batch: Sequence[PoBatchMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: PoBatchMark) -> PoBatchMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
