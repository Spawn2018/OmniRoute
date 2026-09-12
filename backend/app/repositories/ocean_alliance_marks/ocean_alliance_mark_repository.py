from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ocean_alliance_mark import OceanAllianceMark


def _ocean_catalog_query() -> Select[tuple[OceanAllianceMark]]:
    return select(OceanAllianceMark).order_by(
        OceanAllianceMark.mark_code.asc(),
        OceanAllianceMark.created_at.desc(),
    )


class OceanAllianceMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[OceanAllianceMark]:
        loaded = await self._session.scalars(_ocean_catalog_query())
        batch: Sequence[OceanAllianceMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: OceanAllianceMark) -> OceanAllianceMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
