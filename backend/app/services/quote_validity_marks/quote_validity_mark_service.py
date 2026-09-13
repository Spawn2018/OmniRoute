from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.quote_validity_mark import parse_quote_validity_mark_row
from app.models.quote_validity_mark import QuoteValidityMark
from app.repositories.quote_validity_marks.quote_validity_mark_repository import (
    QuoteValidityMarkRepository,
)


class QuoteValidityMarkService:
    """HITL katalog quote validity — bez kolumny quotation i bez daty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = QuoteValidityMarkRepository(session)

    async def list_marks(self) -> list[QuoteValidityMark]:
        return await self._marks.list_marks()

    async def persist_quote_validity_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        validity_kind: object,
        source_ref: object,
    ) -> QuoteValidityMark:
        code, kind, pointer = parse_quote_validity_mark_row(
            mark_code,
            validity_kind,
            source_ref,
        )
        row = QuoteValidityMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            validity_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
