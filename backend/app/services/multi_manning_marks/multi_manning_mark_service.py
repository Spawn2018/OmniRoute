from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.multi_manning_mark import parse_multi_manning_mark_row
from app.models.multi_manning_mark import MultiManningMark
from app.repositories.multi_manning_marks.multi_manning_mark_repository import (
    MultiManningMarkRepository,
)


class MultiManningMarkService:
    """HITL katalog multi-manning — bez tacho live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = MultiManningMarkRepository(session)

    async def list_marks(self) -> list[MultiManningMark]:
        return await self._marks.list_marks()

    async def persist_multi_manning_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        manning_kind: object,
        source_ref: object,
    ) -> MultiManningMark:
        code, kind, pointer = parse_multi_manning_mark_row(
            mark_code,
            manning_kind,
            source_ref,
        )
        row = MultiManningMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            manning_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
