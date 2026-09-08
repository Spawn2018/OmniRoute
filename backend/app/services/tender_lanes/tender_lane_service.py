from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_lane import require_lane_pair, require_lane_source_ref, require_lot_id
from app.models.tender_lane import TenderLane
from app.repositories.tender_lanes.tender_lane_repository import TenderLaneRepository


class TenderLaneService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderLaneRepository(session)

    async def list_marks(self) -> list[TenderLane]:
        return await self._rows.fetch_all()

    async def record_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_lot_id: object,
        origin_unlocode: object,
        destination_unlocode: object,
        source_ref: object,
    ) -> TenderLane:
        origin, dest = require_lane_pair(origin_unlocode, destination_unlocode)
        row = TenderLane(
            id=uuid4(),
            organization_id=organization_id,
            tender_lot_id=require_lot_id(tender_lot_id),
            origin_unlocode=origin,
            destination_unlocode=dest,
            source_ref=require_lane_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
