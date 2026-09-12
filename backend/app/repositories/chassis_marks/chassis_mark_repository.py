from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chassis_mark import ChassisMark


def _chassis_catalog_query() -> Select[tuple[ChassisMark]]:
    return select(ChassisMark).order_by(
        ChassisMark.mark_code.asc(),
        ChassisMark.created_at.desc(),
    )


class ChassisMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ChassisMark]:
        loaded = await self._session.scalars(_chassis_catalog_query())
        batch: Sequence[ChassisMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ChassisMark) -> ChassisMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
