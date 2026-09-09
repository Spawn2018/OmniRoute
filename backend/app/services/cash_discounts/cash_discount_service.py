from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cash_discount import (
    require_cash_discount_source_ref,
    require_discount_kind,
    require_invoice_id,
)
from app.models.cash_discount import CashDiscount
from app.repositories.cash_discounts.cash_discount_repository import (
    CashDiscountRepository,
)


class CashDiscountService:
    def __init__(self, session: AsyncSession) -> None:
        self._discounts = CashDiscountRepository(session)

    async def list_discounts(self) -> list[CashDiscount]:
        return await self._discounts.fetch_discounts()

    async def persist_discount(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sales_invoice_id: object,
        discount_kind: object,
        source_ref: object,
    ) -> CashDiscount:
        row = CashDiscount(
            id=uuid4(),
            organization_id=organization_id,
            sales_invoice_id=require_invoice_id(sales_invoice_id),
            discount_kind=require_discount_kind(discount_kind),
            source_ref=require_cash_discount_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._discounts.add(row)
