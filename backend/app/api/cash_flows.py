from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.bank_payments.bank_payment_service import BankPaymentService
from app.services.cash_flows.cash_flow_service import CashFlowService
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/cash-flows", tags=["cash-flows"])


class CashFlowCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    bank_payment_id: UUID
    source_ref: str


class CashFlowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    bank_payment_id: UUID
    source_ref: str


@router.get("", response_model=list[CashFlowResponse])
async def list_cash_flows(
    _authz: None = Depends(require_permission("can_manage_cash_flows", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CashFlowResponse]:
    rows = await CashFlowService(session).list_flows()
    return [CashFlowResponse.model_validate(row) for row in rows]


@router.post("", response_model=CashFlowResponse, status_code=status.HTTP_201_CREATED)
async def create_cash_flow(
    body: CashFlowCreate,
    _authz: None = Depends(require_permission("can_manage_cash_flows", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CashFlowResponse:
    quotation = await QuotationService(session).get_quotation(body.quotation_id)
    payment = await BankPaymentService(session).get_payment(body.bank_payment_id)
    row = await CashFlowService(session).record_flow(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quotation.id,
        bank_payment_id=payment.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return CashFlowResponse.model_validate(row)
