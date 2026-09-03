from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cash_flow import (
    require_cash_flow_payment_id,
    require_cash_flow_quotation_id,
    require_cash_flow_source_ref,
)
from app.domain.errors import InvalidCashFlow
from app.models.cash_flow import CashFlow
from app.repositories.cash_flows.cash_flow_repository import CashFlowRepository


class CashFlowService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CashFlowRepository(session)

    async def list_flows(self) -> list[CashFlow]:
        return await self._rows.list_all()

    async def record_flow(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        bank_payment_id: UUID,
        source_ref: str,
    ) -> CashFlow:
        row = CashFlow(
            id=uuid4(),
            organization_id=organization_id,
            quotation_id=require_cash_flow_quotation_id(quotation_id),
            bank_payment_id=require_cash_flow_payment_id(bank_payment_id),
            source_ref=require_cash_flow_source_ref(source_ref),
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as orig:
            raise InvalidCashFlow("para już zapisana") from orig
