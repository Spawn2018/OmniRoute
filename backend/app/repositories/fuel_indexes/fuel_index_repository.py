from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fuel_index import FuelIndex


class FuelIndexRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[FuelIndex]:
        result = await self._session.scalars(
            select(FuelIndex).order_by(FuelIndex.published_on.desc(), FuelIndex.id),
        )
        return list(result.all())

    async def get(self, fuel_index_id: UUID) -> FuelIndex | None:
        found = await self._session.get(FuelIndex, fuel_index_id)
        return found if isinstance(found, FuelIndex) else None

    async def add(self, row: FuelIndex) -> FuelIndex:
        self._session.add(row)
        await self._session.flush()
        return row
