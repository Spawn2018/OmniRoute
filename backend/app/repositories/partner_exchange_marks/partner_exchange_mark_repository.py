from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.partner_exchange_mark import PartnerExchangeMark


class PartnerExchangeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PartnerExchangeMark]:
        packed = await self._session.scalars(
            select(PartnerExchangeMark).order_by(
                PartnerExchangeMark.mark_code,
                PartnerExchangeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: PartnerExchangeMark) -> PartnerExchangeMark:
        self._session.add(row)
        await self._session.flush()
        return row
