from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.invoice_match_mark import parse_invoice_match_mark_row
from app.models.invoice_match_mark import InvoiceMatchMark
from app.repositories.invoice_match_marks.invoice_match_mark_repository import (
    InvoiceMatchMarkRepository,
)


class InvoiceMatchMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InvoiceMatchMarkRepository(session)

    async def list_marks(self) -> list[InvoiceMatchMark]:
        return await self._rows.list_marks()

    async def persist_invoice_match_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> InvoiceMatchMark:
        code, kind, origin = parse_invoice_match_mark_row(
            mark_code,
            match_kind,
            source_ref,
        )
        row = InvoiceMatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
