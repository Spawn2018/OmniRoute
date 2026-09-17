from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.purchase_invoice import PurchaseInvoice
from app.services.purchase_invoices.purchase_invoice_service import PurchaseInvoiceService

router = APIRouter(prefix="/purchase-invoices", tags=["purchase-invoices"])

_PERM = "can_manage_purchase_invoices"


class PurchaseInvoiceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invoice_ref: str
    invoice_kind: str
    source_ref: str


class PurchaseInvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    invoice_ref: str
    invoice_kind: str
    source_ref: str


def _row(saved: PurchaseInvoice) -> PurchaseInvoiceResponse:
    return PurchaseInvoiceResponse.model_validate(saved)


@router.get("", response_model=list[PurchaseInvoiceResponse])
async def list_purchase_invoices(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PurchaseInvoiceResponse]:
    packed = await PurchaseInvoiceService(session).list_invoices()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PurchaseInvoiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_purchase_invoice(
    body: PurchaseInvoiceCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PurchaseInvoiceResponse:
    saved = await PurchaseInvoiceService(session).persist_purchase_invoice(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        invoice_ref=body.invoice_ref,
        invoice_kind=body.invoice_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
