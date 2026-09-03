from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/sales-invoices", tags=["sales-invoices"])


class SalesInvoiceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    invoice_kind: str
    invoice_ref: str
    source_ref: str


class SalesInvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    invoice_kind: str
    invoice_ref: str
    source_ref: str


@router.get("", response_model=list[SalesInvoiceResponse])
async def list_sales_invoices(
    _authz: None = Depends(require_permission("can_manage_sales_invoices", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SalesInvoiceResponse]:
    rows = await SalesInvoiceService(session).list_invoices()
    return [SalesInvoiceResponse.model_validate(row) for row in rows]


@router.post(
    "",
    response_model=SalesInvoiceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_sales_invoice(
    body: SalesInvoiceCreate,
    _authz: None = Depends(require_permission("can_manage_sales_invoices", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SalesInvoiceResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await SalesInvoiceService(session).record_invoice(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        invoice_kind=body.invoice_kind,
        invoice_ref=body.invoice_ref,
        source_ref=body.source_ref,
    )
    await session.commit()
    return SalesInvoiceResponse.model_validate(row)
