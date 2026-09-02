from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.customer_rfq import require_rfq_party
from app.domain.money import Money
from app.models.quotation import Quotation
from app.services.customer_rfqs.customer_rfq_service import CustomerRfqService
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["quotations"])


class QuotationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_code: str = Field(min_length=1, max_length=32)
    origin_port_id: UUID
    destination_port_id: UUID
    party_id: UUID
    customer_rfq_id: UUID | None = None


class QuotationBatchCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_codes: list[str] = Field(min_length=1, max_length=20)
    origin_port_id: UUID
    destination_port_id: UUID
    party_id: UUID
    customer_rfq_id: UUID | None = None


class QuotationResponse(BaseModel):
    id: UUID
    organization_id: UUID
    charge_code: str
    rate_line_id: UUID
    amount: str
    currency: str
    source_ref: str
    origin_port_id: UUID | None
    destination_port_id: UUID | None
    party_id: UUID | None
    customer_rfq_id: UUID | None

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
            origin_port_id=row.origin_port_id,
            destination_port_id=row.destination_port_id,
            party_id=row.party_id,
            customer_rfq_id=row.customer_rfq_id,
        )


async def _quote_customer_rfq_id(
    session: AsyncSession,
    customer_rfq_id: UUID | None,
    party_id: UUID,
) -> UUID | None:
    if customer_rfq_id is None:
        return None
    rfq = await CustomerRfqService(session).get_rfq(customer_rfq_id)
    require_rfq_party(rfq.party_id, party_id)
    return rfq.id


@router.get("", response_model=list[QuotationResponse])
async def list_quotations(
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    party_id: UUID | None = Query(default=None),
    origin_port_id: UUID | None = Query(default=None),
    destination_port_id: UUID | None = Query(default=None),
    customer_rfq_id: UUID | None = Query(default=None),
) -> list[QuotationResponse]:
    service = QuotationService(session)
    rows = await service.list_quotations(
        party_id=party_id,
        origin_port_id=origin_port_id,
        destination_port_id=destination_port_id,
        customer_rfq_id=customer_rfq_id,
    )
    return [QuotationResponse.from_row(row) for row in rows]


@router.post("", response_model=QuotationResponse, status_code=status.HTTP_201_CREATED)
async def create_quotation(
    body: QuotationCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuotationResponse:
    service = QuotationService(session)
    linked_rfq_id = await _quote_customer_rfq_id(
        session,
        body.customer_rfq_id,
        body.party_id,
    )
    row = await service.quote_from_current_rate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_code=body.charge_code,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        party_id=body.party_id,
        customer_rfq_id=linked_rfq_id,
    )
    await session.commit()
    return QuotationResponse.from_row(row)


@router.post("/batch", response_model=list[QuotationResponse], status_code=status.HTTP_201_CREATED)
async def create_quotation_batch(
    body: QuotationBatchCreate,
    _authz: None = Depends(require_permission("can_manage_quotations", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> list[QuotationResponse]:
    service = QuotationService(session)
    linked_rfq_id = await _quote_customer_rfq_id(
        session,
        body.customer_rfq_id,
        body.party_id,
    )
    rows = await service.quote_batch_from_current_rates(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_codes=body.charge_codes,
        origin_port_id=body.origin_port_id,
        destination_port_id=body.destination_port_id,
        party_id=body.party_id,
        customer_rfq_id=linked_rfq_id,
    )
    await session.commit()
    return [QuotationResponse.from_row(row) for row in rows]
