from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.terms_ai_mark import parse_terms_ai_mark_row
from app.models.terms_ai_mark import TermsAiMark
from app.repositories.terms_ai_marks.terms_ai_mark_repository import (
    TermsAiMarkRepository,
)


class TermsAiMarkService:
    """HITL katalog Terms AI — bez terms live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = TermsAiMarkRepository(session)

    async def list_marks(self) -> list[TermsAiMark]:
        return await self._marks.list_marks()

    async def persist_terms_ai_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        terms_kind: object,
        source_ref: object,
    ) -> TermsAiMark:
        code, kind, pointer = parse_terms_ai_mark_row(
            mark_code,
            terms_kind,
            source_ref,
        )
        row = TermsAiMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            terms_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
