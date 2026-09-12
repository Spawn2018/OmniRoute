from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demo_gps_mark import DemoGpsMark


def _demo_gps_catalog_query() -> Select[tuple[DemoGpsMark]]:
    return select(DemoGpsMark).order_by(
        DemoGpsMark.mark_code.asc(),
        DemoGpsMark.created_at.desc(),
    )


class DemoGpsMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DemoGpsMark]:
        loaded = await self._session.scalars(_demo_gps_catalog_query())
        batch: Sequence[DemoGpsMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: DemoGpsMark) -> DemoGpsMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
