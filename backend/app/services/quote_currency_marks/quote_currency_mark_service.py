from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.quote_currency_mark import parse_quote_currency_mark_row
from app.models.quote_currency_mark import QuoteCurrencyMark
from app.repositories.quote_currency_marks.quote_currency_mark_repository import (
    QuoteCurrencyMarkRepository,
)


class QuoteCurrencyMarkService:
    """HITL katalog quote currency — bez kolumny quotation i bez NBP."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = QuoteCurrencyMarkRepository(session)

    async def list_marks(self) -> list[QuoteCurrencyMark]:
        return await self._marks.list_marks()

    async def persist_quote_currency_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        currency_kind: object,
        source_ref: object,
    ) -> QuoteCurrencyMark:
        code, kind, pointer = parse_quote_currency_mark_row(
            mark_code,
            currency_kind,
            source_ref,
        )
        row = QuoteCurrencyMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            currency_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
