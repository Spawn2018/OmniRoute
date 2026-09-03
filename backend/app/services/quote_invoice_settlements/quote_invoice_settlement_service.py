from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidQuoteInvoiceSettlement
from app.domain.quote_invoice_settlement import (
    require_settlement_invoice_id,
    require_settlement_quotation_id,
    require_settlement_source_ref,
)
from app.models.quote_invoice_settlement import QuoteInvoiceSettlement
from app.repositories.quote_invoice_settlements.quote_invoice_settlement_repository import (
    QuoteInvoiceSettlementRepository,
)


class QuoteInvoiceSettlementService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = QuoteInvoiceSettlementRepository(session)

    async def list_settlements(self) -> list[QuoteInvoiceSettlement]:
        return await self._rows.list_all()

    async def record_settlement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        sales_invoice_id: UUID,
        source_ref: str,
    ) -> QuoteInvoiceSettlement:
        row = QuoteInvoiceSettlement(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_settlement_quotation_id(quotation_id),
            sales_invoice_id=require_settlement_invoice_id(sales_invoice_id),
            source_ref=require_settlement_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidQuoteInvoiceSettlement("para już zapisana") from orig
