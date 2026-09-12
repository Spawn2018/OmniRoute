from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.posting_mark import parse_posting_mark_row
from app.models.posting_mark import PostingMark
from app.repositories.posting_marks.posting_mark_repository import (
    PostingMarkRepository,
)


class PostingMarkService:
    """HITL katalog posting — bez posting live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = PostingMarkRepository(session)

    async def list_marks(self) -> list[PostingMark]:
        return await self._marks.list_marks()

    async def persist_posting_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        posting_kind: object,
        source_ref: object,
    ) -> PostingMark:
        code, kind, pointer = parse_posting_mark_row(
            mark_code,
            posting_kind,
            source_ref,
        )
        row = PostingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            posting_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
