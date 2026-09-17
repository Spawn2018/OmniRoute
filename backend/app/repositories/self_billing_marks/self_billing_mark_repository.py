from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.self_billing_mark import SelfBillingMark


class SelfBillingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SelfBillingMark]:
        packed = await self._session.scalars(
            select(SelfBillingMark).order_by(
                SelfBillingMark.mark_code,
                SelfBillingMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SelfBillingMark) -> SelfBillingMark:
        self._session.add(row)
        await self._session.flush()
        return row
