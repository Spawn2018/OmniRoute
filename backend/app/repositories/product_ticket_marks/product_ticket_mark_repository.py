from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_ticket_mark import ProductTicketMark


class ProductTicketMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ProductTicketMark]:
        stmt = select(ProductTicketMark).order_by(
            ProductTicketMark.mark_code,
            ProductTicketMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: ProductTicketMark) -> ProductTicketMark:
        self._session.add(row)
        await self._session.flush()
        return row
