from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cash_discount import CashDiscount


class CashDiscountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_discounts(self) -> list[CashDiscount]:
        packed = await self._session.scalars(
            select(CashDiscount).order_by(
                CashDiscount.created_at.desc(),
                CashDiscount.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: CashDiscount) -> CashDiscount:
        self._session.add(row)
        await self._session.flush()
        return row
