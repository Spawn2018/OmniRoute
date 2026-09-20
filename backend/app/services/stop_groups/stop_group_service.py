from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.stop_group import (
    require_stop_group_code,
    require_stop_group_shipment_id,
    require_stop_group_source_ref,
)
from app.models.stop_group import StopGroup
from app.repositories.stop_groups.stop_group_repository import StopGroupRepository


class StopGroupService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = StopGroupRepository(session)

    async def list_groups(self) -> list[StopGroup]:
        return await self._rows.list_all()

    async def record_group(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        group_code: object,
        source_ref: object,
    ) -> StopGroup:
        row = StopGroup(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_stop_group_shipment_id(shipment_id),
            group_code=require_stop_group_code(group_code),
            source_ref=require_stop_group_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
