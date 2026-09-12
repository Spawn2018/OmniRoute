from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lez_mark import parse_lez_mark_row
from app.models.lez_mark import LezMark
from app.repositories.lez_marks.lez_mark_repository import (
    LezMarkRepository,
)


class LezMarkService:
    """HITL katalog LEZ — bez LEZ live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = LezMarkRepository(session)

    async def list_marks(self) -> list[LezMark]:
        return await self._marks.list_marks()

    async def persist_lez_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        lez_kind: object,
        source_ref: object,
    ) -> LezMark:
        code, kind, pointer = parse_lez_mark_row(
            mark_code,
            lez_kind,
            source_ref,
        )
        row = LezMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            lez_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
