from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sales_lane import parse_sales_lane_row
from app.models.sales_lane import SalesLane
from app.repositories.sales_lanes.sales_lane_repository import (
    SalesLaneRepository,
)


class SalesLaneService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SalesLaneRepository(session)

    async def list_lanes(self) -> list[SalesLane]:
        return await self._rows.list_lanes()

    async def persist_sales_lane(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        lane_code: object,
        lane_kind: object,
        source_ref: object,
    ) -> SalesLane:
        code, kind, origin = parse_sales_lane_row(
            lane_code,
            lane_kind,
            source_ref,
        )
        row = SalesLane(
            id=uuid4(),
            organization_id=organization_id,
            lane_code=code,
            lane_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_lane(row)
