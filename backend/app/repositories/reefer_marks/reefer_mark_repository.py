from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reefer_mark import ReeferMark


def _reefer_catalog_query() -> Select[tuple[ReeferMark]]:
    return select(ReeferMark).order_by(
        ReeferMark.mark_code.asc(),
        ReeferMark.created_at.desc(),
    )


class ReeferMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ReeferMark]:
        loaded = await self._session.scalars(_reefer_catalog_query())
        batch: Sequence[ReeferMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ReeferMark) -> ReeferMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
