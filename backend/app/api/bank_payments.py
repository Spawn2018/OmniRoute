from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.bank_payments.bank_payment_service import BankPaymentService
from app.services.parties.party_service import PartyService
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService

router = APIRouter(prefix="/bank-payments", tags=["bank-payments"])


class BankPaymentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sales_invoice_id: UUID
    party_bank_account_id: UUID
    source_ref: str


class BankPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    sales_invoice_id: UUID
    party_bank_account_id: UUID
    source_ref: str


@router.get("", response_model=list[BankPaymentResponse])
async def list_bank_payments(
    _authz: None = Depends(require_permission("can_manage_bank_payments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BankPaymentResponse]:
    rows = await BankPaymentService(session).list_payments()
    return [BankPaymentResponse.model_validate(row) for row in rows]


@router.post("", response_model=BankPaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_bank_payment(
    body: BankPaymentCreate,
    _authz: None = Depends(require_permission("can_manage_bank_payments", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BankPaymentResponse:
    invoice = await SalesInvoiceService(session).get_invoice(body.sales_invoice_id)
    account = await PartyService(session).get_bank_account(body.party_bank_account_id)
    row = await BankPaymentService(session).record_payment(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        sales_invoice_id=invoice.id,
        party_bank_account_id=account.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return BankPaymentResponse.model_validate(row)
