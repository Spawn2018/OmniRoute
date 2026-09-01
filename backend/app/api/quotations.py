from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.money import Money
from app.models.quotation import Quotation
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["quotations"])


class QuotationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_code: str = Field(min_length=1, max_length=32)


class QuotationResponse(BaseModel):
    id: UUID
    organization_id: UUID
    charge_code: str
    rate_line_id: UUID
    amount: str
    currency: str
    source_ref: str

    @classmethod
    def from_row(cls, row: Quotation) -> "QuotationResponse":
        money = Money.of(row.amount, row.currency)
        amount_text, currency = money.as_pair()
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            charge_code=row.charge_code,
            rate_line_id=row.rate_line_id,
            amount=amount_text,
            currency=currency,
            source_ref=row.source_ref,
        )


@router.get("", response_model=list[QuotationResponse])
async def list_quotations(
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[QuotationResponse]:
    service = QuotationService(session)
    rows = await service.list_quotations()
    return [QuotationResponse.from_row(row) for row in rows]


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(
    body: QuotationCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuotationResponse:
    service = QuotationService(session)
    row = await service.quote_from_current_rate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_code=body.charge_code,
    )
    await session.commit()
    return QuotationResponse.from_row(row)
