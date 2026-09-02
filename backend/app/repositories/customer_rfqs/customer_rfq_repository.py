from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer_rfq import CustomerRfq


class CustomerRfqRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[CustomerRfq]:
        result = await self._session.scalars(
            select(CustomerRfq).order_by(CustomerRfq.created_at.desc()),
        )
        return list(result.all())

    async def get(self, rfq_id: UUID) -> CustomerRfq | None:
        found = await self._session.get(CustomerRfq, rfq_id)
        return found if isinstance(found, CustomerRfq) else None

    async def add(self, row: CustomerRfq) -> CustomerRfq:
        self._session.add(row)
        await self._session.flush()
        return row
