from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bank_payment import BankPayment


class BankPaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, payment_id: UUID) -> BankPayment | None:
        return await self._session.get(BankPayment, payment_id)

    async def list_all(self) -> list[BankPayment]:
        result = await self._session.scalars(
            select(BankPayment).order_by(BankPayment.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: BankPayment) -> BankPayment:
        self._session.add(row)
        await self._session.flush()
        return row
