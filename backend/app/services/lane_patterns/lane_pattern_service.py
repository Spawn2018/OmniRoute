from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lane_pattern import require_pattern_pair, require_pattern_source_ref
from app.models.lane_pattern import LanePattern
from app.repositories.lane_patterns.lane_pattern_repository import LanePatternRepository


class LanePatternService:
    def __init__(self, session: AsyncSession) -> None:
        self._patterns = LanePatternRepository(session)

    async def list_patterns(self) -> list[LanePattern]:
        return await self._patterns.fetch_patterns()

    async def persist_pattern(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        origin_unlocode: object,
        destination_unlocode: object,
        source_ref: object,
    ) -> LanePattern:
        origin, dest = require_pattern_pair(origin_unlocode, destination_unlocode)
        row = LanePattern(
            id=uuid4(),
            organization_id=organization_id,
            origin_unlocode=origin,
            destination_unlocode=dest,
            source_ref=require_pattern_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._patterns.add(row)
