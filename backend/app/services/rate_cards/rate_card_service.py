from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rate_card import (
    require_applies_when,
    require_card_amount,
    require_card_code,
    require_card_currency,
    require_card_source_ref,
)
from app.models.rate_card import RateCard
from app.repositories.rate_cards.rate_card_repository import RateCardRepository


class RateCardService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RateCardRepository(session)

    async def list_cards(self) -> list[RateCard]:
        return await self._rows.list_all()

    async def record_card(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        card_code: object,
        applies_when: object,
        amount: object,
        currency: object,
        source_ref: object,
    ) -> RateCard:
        row = RateCard(
            id=uuid4(),
            organization_id=organization_id,
            card_code=require_card_code(card_code),
            applies_when=require_applies_when(applies_when),
            amount=require_card_amount(amount),
            currency=require_card_currency(currency),
            source_ref=require_card_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
