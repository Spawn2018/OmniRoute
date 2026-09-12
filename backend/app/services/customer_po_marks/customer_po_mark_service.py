from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.customer_po_mark import parse_customer_po_mark_row
from app.models.customer_po_mark import CustomerPoMark
from app.repositories.customer_po_marks.customer_po_mark_repository import (
    CustomerPoMarkRepository,
)


class CustomerPoMarkService:
    """HITL katalog referencji PO klienta — bez purchase_order CT1 i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = CustomerPoMarkRepository(session)

    async def list_marks(self) -> list[CustomerPoMark]:
        return await self._marks.list_marks()

    async def persist_customer_po_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ref_kind: object,
        source_ref: object,
    ) -> CustomerPoMark:
        code, kind, pointer = parse_customer_po_mark_row(
            mark_code,
            ref_kind,
            source_ref,
        )
        row = CustomerPoMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ref_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
