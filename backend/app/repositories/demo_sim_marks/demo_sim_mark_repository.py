from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demo_sim_mark import DemoSimMark


def _demo_sim_catalog_query() -> Select[tuple[DemoSimMark]]:
    return select(DemoSimMark).order_by(
        DemoSimMark.mark_code.asc(),
        DemoSimMark.created_at.desc(),
    )


class DemoSimMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DemoSimMark]:
        loaded = await self._session.scalars(_demo_sim_catalog_query())
        batch: Sequence[DemoSimMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: DemoSimMark) -> DemoSimMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
