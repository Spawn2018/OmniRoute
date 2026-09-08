from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fuel_index import (
    require_index_kind,
    require_index_source_ref,
    require_index_value,
    require_published_on,
)
from app.models.fuel_index import FuelIndex
from app.repositories.fuel_indexes.fuel_index_repository import FuelIndexRepository


class FuelIndexService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FuelIndexRepository(session)

    async def list_indexes(self) -> list[FuelIndex]:
        return await self._rows.list_all()

    async def record_index(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        index_kind: object,
        published_on: object,
        index_value: object,
        source_ref: object,
    ) -> FuelIndex:
        row = FuelIndex(
            id=uuid4(),
            organization_id=organization_id,
            index_kind=require_index_kind(index_kind),
            published_on=require_published_on(published_on),
            index_value=require_index_value(index_value),
            source_ref=require_index_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
