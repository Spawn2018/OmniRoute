from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.tender_quote import TenderQuote
from app.services.quotations.quotation_service import QuotationService
from app.services.tender_quotes.tender_quote_service import TenderQuoteService

router = APIRouter(prefix="/tender-quotes", tags=["tender-quotes"])

_PERM = "can_manage_tender_quotes"


class TenderQuoteCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    valid_until: str
    order_limit: int
    source_ref: str


class TenderQuoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    valid_until: str
    order_limit: int
    source_ref: str


def _as_row(row: TenderQuote) -> TenderQuoteResponse:
    return TenderQuoteResponse(
        id=row.id,
        organization_id=row.organization_id,
        quotation_id=row.quotation_id,
        valid_until=row.valid_until.isoformat(),
        order_limit=row.order_limit,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[TenderQuoteResponse])
async def list_tender_quotes(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TenderQuoteResponse]:
    rows = await TenderQuoteService(session).list_bids()
    return [_as_row(row) for row in rows]


@router.post("", response_model=TenderQuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_tender_quote(
    body: TenderQuoteCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TenderQuoteResponse:
    offer = await QuotationService(session).get_quotation(body.quotation_id)
    row = await TenderQuoteService(session).record_bid(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=offer.id,
        valid_until=body.valid_until,
        order_limit=body.order_limit,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
