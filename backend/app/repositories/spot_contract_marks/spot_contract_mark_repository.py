from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.spot_contract_mark import SpotContractMark


def _spot_contract_catalog_query() -> Select[tuple[SpotContractMark]]:
    return select(SpotContractMark).order_by(
        SpotContractMark.mark_code.asc(),
        SpotContractMark.created_at.desc(),
    )


class SpotContractMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SpotContractMark]:
        loaded = await self._session.scalars(_spot_contract_catalog_query())
        batch: Sequence[SpotContractMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: SpotContractMark) -> SpotContractMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
