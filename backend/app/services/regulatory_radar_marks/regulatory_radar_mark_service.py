from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.regulatory_radar_mark import parse_regulatory_radar_mark_row
from app.models.regulatory_radar_mark import RegulatoryRadarMark
from app.repositories.regulatory_radar_marks.regulatory_radar_mark_repository import (
    RegulatoryRadarMarkRepository,
)


class RegulatoryRadarMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RegulatoryRadarMarkRepository(session)

    async def list_marks(self) -> list[RegulatoryRadarMark]:
        return await self._rows.list_marks()

    async def persist_regulatory_radar_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        radar_kind: object,
        source_ref: object,
    ) -> RegulatoryRadarMark:
        code, kind, origin = parse_regulatory_radar_mark_row(
            mark_code,
            radar_kind,
            source_ref,
        )
        row = RegulatoryRadarMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            radar_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
