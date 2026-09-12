from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.reefer_mark import parse_reefer_mark_row
from app.models.reefer_mark import ReeferMark
from app.repositories.reefer_marks.reefer_mark_repository import (
    ReeferMarkRepository,
)


class ReeferMarkService:
    """HITL katalog reefer — bez reefer live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ReeferMarkRepository(session)

    async def list_marks(self) -> list[ReeferMark]:
        return await self._marks.list_marks()

    async def persist_reefer_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        reefer_kind: object,
        source_ref: object,
    ) -> ReeferMark:
        code, kind, pointer = parse_reefer_mark_row(
            mark_code,
            reefer_kind,
            source_ref,
        )
        row = ReeferMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            reefer_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
