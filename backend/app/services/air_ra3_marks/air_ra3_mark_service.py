from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.air_ra3_mark import parse_air_ra3_mark_row
from app.models.air_ra3_mark import AirRa3Mark
from app.repositories.air_ra3_marks.air_ra3_mark_repository import AirRa3MarkRepository


class AirRa3MarkService:
    """HITL katalog CSRD — bez kg/tCO2e i bez live filing."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = AirRa3MarkRepository(session)

    async def list_marks(self) -> list[AirRa3Mark]:
        return await self._marks.list_marks()

    async def persist_air_ra3_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        air_kind: object,
        source_ref: object,
    ) -> AirRa3Mark:
        code, kind, pointer = parse_air_ra3_mark_row(mark_code, air_kind, source_ref)
        row = AirRa3Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            air_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
