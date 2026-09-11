from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.billing_mark import BillingMark


class BillingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BillingMark]:
        packed = await self._session.scalars(
            select(BillingMark).order_by(
                BillingMark.mark_code,
                BillingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: BillingMark) -> BillingMark:
        self._session.add(row)
        await self._session.flush()
        return row
