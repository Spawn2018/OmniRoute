from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.nvocc_mark import parse_nvocc_mark_row
from app.models.nvocc_mark import NvoccMark
from app.repositories.nvocc_marks.nvocc_mark_repository import (
    NvoccMarkRepository,
)


class NvoccMarkService:
    """HITL katalog NVOCC — bez nvocc live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = NvoccMarkRepository(session)

    async def list_marks(self) -> list[NvoccMark]:
        return await self._marks.list_marks()

    async def persist_nvocc_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        nvocc_kind: object,
        source_ref: object,
    ) -> NvoccMark:
        code, kind, pointer = parse_nvocc_mark_row(
            mark_code,
            nvocc_kind,
            source_ref,
        )
        row = NvoccMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            nvocc_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
