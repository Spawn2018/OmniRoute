from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lane_km import require_km_code, require_lane_km, require_lane_source_ref
from app.models.lane_km import LaneKm
from app.repositories.lane_kms.lane_km_repository import LaneKmRepository


class LaneKmService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LaneKmRepository(session)

    async def list_rows(self) -> list[LaneKm]:
        return await self._rows.fetch_rows()

    async def persist_lane_km(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        km_code: object,
        loaded_km: object,
        empty_km: object,
        approach_km: object,
        source_ref: object,
    ) -> LaneKm:
        row = LaneKm(
            id=uuid4(),
            organization_id=organization_id,
            km_code=require_km_code(km_code),
            loaded_km=require_lane_km(loaded_km, "ladowny"),
            empty_km=require_lane_km(empty_km, "pusty"),
            approach_km=require_lane_km(approach_km, "dolot"),
            source_ref=require_lane_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
