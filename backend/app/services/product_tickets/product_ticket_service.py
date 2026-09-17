from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.product_ticket import parse_product_ticket_row
from app.models.product_ticket import ProductTicket
from app.repositories.product_tickets.product_ticket_repository import (
    ProductTicketRepository,
)


class ProductTicketService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ProductTicketRepository(session)

    async def list_tickets(self) -> list[ProductTicket]:
        return await self._rows.list_tickets()

    async def get_ticket(self, ticket_id: UUID) -> ProductTicket:
        found = await self._rows.get_ticket(ticket_id)
        if found is None:
            raise ResourceNotFound(f"nieznany ticket produktu: {ticket_id}")
        return found

    async def persist_product_ticket(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        ticket_code: object,
        title: object,
        body: object,
        ticket_kind: object,
        source_ref: object,
    ) -> ProductTicket:
        code, heading, text, kind, origin = parse_product_ticket_row(
            ticket_code,
            title,
            body,
            ticket_kind,
            source_ref,
        )
        row = ProductTicket(
            id=uuid4(),
            organization_id=organization_id,
            ticket_code=code,
            title=heading,
            body=text,
            ticket_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_ticket(row)
