from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ocean_alliance_mark import parse_ocean_alliance_mark_row
from app.models.ocean_alliance_mark import OceanAllianceMark
from app.repositories.ocean_alliance_marks.ocean_alliance_mark_repository import (
    OceanAllianceMarkRepository,
)


class OceanAllianceMarkService:
    """HITL katalog ocean alliance — bez live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = OceanAllianceMarkRepository(session)

    async def list_marks(self) -> list[OceanAllianceMark]:
        return await self._marks.list_marks()

    async def persist_ocean_alliance_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ocean_kind: object,
        source_ref: object,
    ) -> OceanAllianceMark:
        code, kind, pointer = parse_ocean_alliance_mark_row(
            mark_code,
            ocean_kind,
            source_ref,
        )
        row = OceanAllianceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ocean_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
