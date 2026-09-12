from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer_po_mark import CustomerPoMark


def _customer_po_catalog_query() -> Select[tuple[CustomerPoMark]]:
    return select(CustomerPoMark).order_by(
        CustomerPoMark.mark_code.asc(),
        CustomerPoMark.created_at.desc(),
    )


class CustomerPoMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CustomerPoMark]:
        loaded = await self._session.scalars(_customer_po_catalog_query())
        batch: Sequence[CustomerPoMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: CustomerPoMark) -> CustomerPoMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
