from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ocean_feeder_mark import parse_ocean_feeder_mark_row
from app.models.ocean_feeder_mark import OceanFeederMark
from app.repositories.ocean_feeder_marks.ocean_feeder_mark_repository import (
    OceanFeederMarkRepository,
)


class OceanFeederMarkService:
    """HITL katalog feeder/short-sea — bez live schedule i bez TEU."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = OceanFeederMarkRepository(session)

    async def list_marks(self) -> list[OceanFeederMark]:
        return await self._marks.list_marks()

    async def persist_ocean_feeder_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        feeder_kind: object,
        source_ref: object,
    ) -> OceanFeederMark:
        code, kind, pointer = parse_ocean_feeder_mark_row(
            mark_code,
            feeder_kind,
            source_ref,
        )
        row = OceanFeederMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            feeder_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
