from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rate_card import RateCard


class RateCardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[RateCard]:
        result = await self._session.scalars(
            select(RateCard).order_by(RateCard.created_at.desc(), RateCard.id),
        )
        return list(result.all())

    async def fetch_equal_when(self, applies_when: str) -> list[RateCard]:
        result = await self._session.scalars(
            select(RateCard)
            .where(RateCard.applies_when == applies_when)
            .order_by(RateCard.card_code, RateCard.id),
        )
        return list(result.all())

    async def add(self, row: RateCard) -> RateCard:
        self._session.add(row)
        await self._session.flush()
        return row
