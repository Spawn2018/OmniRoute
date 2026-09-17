from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.invoice_alloc_mark import parse_invoice_alloc_mark_row
from app.models.invoice_alloc_mark import InvoiceAllocMark
from app.repositories.invoice_alloc_marks.invoice_alloc_mark_repository import (
    InvoiceAllocMarkRepository,
)


class InvoiceAllocMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InvoiceAllocMarkRepository(session)

    async def list_marks(self) -> list[InvoiceAllocMark]:
        return await self._rows.list_marks()

    async def persist_invoice_alloc_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        alloc_kind: object,
        source_ref: object,
    ) -> InvoiceAllocMark:
        code, kind, origin = parse_invoice_alloc_mark_row(
            mark_code,
            alloc_kind,
            source_ref,
        )
        row = InvoiceAllocMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            alloc_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
