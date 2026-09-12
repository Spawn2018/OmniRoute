from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.demo_wipe_mark import DemoWipeMark


def _demo_wipe_catalog_query() -> Select[tuple[DemoWipeMark]]:
    return select(DemoWipeMark).order_by(
        DemoWipeMark.mark_code.asc(),
        DemoWipeMark.created_at.desc(),
    )


class DemoWipeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DemoWipeMark]:
        loaded = await self._session.scalars(_demo_wipe_catalog_query())
        batch: Sequence[DemoWipeMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: DemoWipeMark) -> DemoWipeMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
