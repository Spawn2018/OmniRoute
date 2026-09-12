from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.air_ra3_mark import AirRa3Mark


def _csrd_catalog_query() -> Select[tuple[AirRa3Mark]]:
    return select(AirRa3Mark).order_by(AirRa3Mark.mark_code.asc(), AirRa3Mark.created_at.desc())


class AirRa3MarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[AirRa3Mark]:
        loaded = await self._session.scalars(_csrd_catalog_query())
        batch: Sequence[AirRa3Mark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: AirRa3Mark) -> AirRa3Mark:
        self._session.add(entity)
        await self._session.flush()
        return entity
