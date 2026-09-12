from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tacho_office_mark import parse_tacho_office_mark_row
from app.models.tacho_office_mark import TachoOfficeMark
from app.repositories.tacho_office_marks.tacho_office_mark_repository import (
    TachoOfficeMarkRepository,
)


class TachoOfficeMarkService:
    """HITL katalog tacho office — bez tacho live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = TachoOfficeMarkRepository(session)

    async def list_marks(self) -> list[TachoOfficeMark]:
        return await self._marks.list_marks()

    async def persist_tacho_office_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        tacho_kind: object,
        source_ref: object,
    ) -> TachoOfficeMark:
        code, kind, pointer = parse_tacho_office_mark_row(
            mark_code,
            tacho_kind,
            source_ref,
        )
        row = TachoOfficeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            tacho_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
