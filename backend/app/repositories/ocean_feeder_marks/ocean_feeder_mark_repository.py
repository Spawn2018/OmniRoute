from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ocean_feeder_mark import OceanFeederMark


def _ocean_feeder_catalog_query() -> Select[tuple[OceanFeederMark]]:
    return select(OceanFeederMark).order_by(
        OceanFeederMark.mark_code.asc(),
        OceanFeederMark.created_at.desc(),
    )


class OceanFeederMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OceanFeederMark]:
        loaded = await self._session.scalars(_ocean_feeder_catalog_query())
        batch: Sequence[OceanFeederMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: OceanFeederMark) -> OceanFeederMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
