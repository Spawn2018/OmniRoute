from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.invoice_match_mark import InvoiceMatchMark


class InvoiceMatchMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[InvoiceMatchMark]:
        packed = await self._session.scalars(
            select(InvoiceMatchMark).order_by(
                InvoiceMatchMark.mark_code,
                InvoiceMatchMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: InvoiceMatchMark) -> InvoiceMatchMark:
        self._session.add(row)
        await self._session.flush()
        return row
