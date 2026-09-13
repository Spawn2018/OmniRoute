from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.autonomy_level import AutonomyLevel


def _level_query() -> Select[tuple[AutonomyLevel]]:
    return select(AutonomyLevel).order_by(AutonomyLevel.created_at.desc(), AutonomyLevel.id)


class AutonomyLevelRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[AutonomyLevel]:
        loaded = await self._session.scalars(_level_query())
        batch: Sequence[AutonomyLevel] = loaded.all()
        return list(batch)

    async def add(self, entity: AutonomyLevel) -> AutonomyLevel:
        self._session.add(entity)
        await self._session.flush()
        return entity
