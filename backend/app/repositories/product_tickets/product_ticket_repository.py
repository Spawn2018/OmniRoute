from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_ticket import ProductTicket


class ProductTicketRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_tickets(self) -> list[ProductTicket]:
        stmt = select(ProductTicket).order_by(
            ProductTicket.ticket_code,
            ProductTicket.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_ticket(self, row: ProductTicket) -> ProductTicket:
        self._session.add(row)
        await self._session.flush()
        return row
