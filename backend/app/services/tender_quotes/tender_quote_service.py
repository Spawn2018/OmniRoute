from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_quote import (
    require_bid_source_ref,
    require_order_limit,
    require_quote_id,
    require_valid_until,
)
from app.models.tender_quote import TenderQuote
from app.repositories.tender_quotes.tender_quote_repository import TenderQuoteRepository


class TenderQuoteService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderQuoteRepository(session)

    async def list_bids(self) -> list[TenderQuote]:
        return await self._rows.list_all()

    async def record_bid(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: object,
        valid_until: object,
        order_limit: object,
        source_ref: object,
    ) -> TenderQuote:
        row = TenderQuote(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_quote_id(quotation_id),
            valid_until=require_valid_until(valid_until),
            order_limit=require_order_limit(order_limit),
            source_ref=require_bid_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
