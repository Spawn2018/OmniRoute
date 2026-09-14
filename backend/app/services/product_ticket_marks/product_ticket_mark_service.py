from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.product_ticket_mark import parse_product_ticket_mark_row
from app.models.product_ticket_mark import ProductTicketMark
from app.repositories.product_ticket_marks.product_ticket_mark_repository import (
    ProductTicketMarkRepository,
)


class ProductTicketMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ProductTicketMarkRepository(session)

    async def list_marks(self) -> list[ProductTicketMark]:
        return await self._rows.list_marks()

    async def persist_product_ticket_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ticket_kind: object,
        source_ref: object,
    ) -> ProductTicketMark:
        code, kind, origin = parse_product_ticket_mark_row(
            mark_code,
            ticket_kind,
            source_ref,
        )
        row = ProductTicketMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ticket_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
