from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.quotations.quotation_service import QuotationService
from app.services.quote_invoice_settlements.quote_invoice_settlement_service import (
    QuoteInvoiceSettlementService,
)
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService

router = APIRouter(prefix="/quote-invoice-settlements", tags=["quote-invoice-settlements"])


class QuoteInvoiceSettlementCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    sales_invoice_id: UUID
    source_ref: str


class QuoteInvoiceSettlementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    sales_invoice_id: UUID
    source_ref: str


@router.get("", response_model=list[QuoteInvoiceSettlementResponse])
async def list_quote_invoice_settlements(
    _authz: None = Depends(
        require_permission("can_manage_quote_invoice_settlements", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[QuoteInvoiceSettlementResponse]:
    rows = await QuoteInvoiceSettlementService(session).list_settlements()
    return [QuoteInvoiceSettlementResponse.model_validate(row) for row in rows]


@router.post(
    "",
    response_model=QuoteInvoiceSettlementResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_quote_invoice_settlement(
    body: QuoteInvoiceSettlementCreate,
    _authz: None = Depends(
        require_permission("can_manage_quote_invoice_settlements", "organization"),
    ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> QuoteInvoiceSettlementResponse:
    quotation = await QuotationService(session).get_quotation(body.quotation_id)
    invoice = await SalesInvoiceService(session).get_invoice(body.sales_invoice_id)
    row = await QuoteInvoiceSettlementService(session).record_settlement(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quotation.id,
        sales_invoice_id=invoice.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return QuoteInvoiceSettlementResponse.model_validate(row)
