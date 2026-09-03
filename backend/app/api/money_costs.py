from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.bank_payments.bank_payment_service import BankPaymentService
from app.services.money_costs.money_cost_service import MoneyCostService
from app.services.nbp_rates.nbp_rate_service import NbpRateService

router = APIRouter(prefix="/money-costs", tags=["money-costs"])


class MoneyCostCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    bank_payment_id: UUID
    nbp_rate_id: UUID
    source_ref: str


class MoneyCostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    bank_payment_id: UUID
    nbp_rate_id: UUID
    source_ref: str


@router.get("", response_model=list[MoneyCostResponse])
async def list_money_costs(
    _authz: None = Depends(require_permission("can_manage_money_costs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MoneyCostResponse]:
    rows = await MoneyCostService(session).list_costs()
    return [MoneyCostResponse.model_validate(row) for row in rows]


@router.post("", response_model=MoneyCostResponse, status_code=status.HTTP_201_CREATED)
async def create_money_cost(
    body: MoneyCostCreate,
    _authz: None = Depends(require_permission("can_manage_money_costs", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MoneyCostResponse:
    payment = await BankPaymentService(session).get_payment(body.bank_payment_id)
    rate = await NbpRateService(session).get_rate(body.nbp_rate_id)
    row = await MoneyCostService(session).record_cost(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        bank_payment_id=payment.id,
        nbp_rate_id=rate.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return MoneyCostResponse.model_validate(row)
