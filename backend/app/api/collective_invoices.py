from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.collective_invoice import (
    require_collective_extra_shipment,
    require_collective_same_party,
)
from app.services.collective_invoices.collective_invoice_service import CollectiveInvoiceService
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService
from app.services.shipments.shipment_service import ShipmentService

router = APIRouter(prefix="/collective-invoices", tags=["collective-invoices"])


class CollectiveInvoiceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sales_invoice_id: UUID
    shipment_id: UUID
    source_ref: str


class CollectiveInvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    sales_invoice_id: UUID
    shipment_id: UUID
    source_ref: str


@router.get("", response_model=list[CollectiveInvoiceResponse])
async def list_collective_invoices(
    _authz: None = Depends(require_permission("can_manage_collective_invoices", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CollectiveInvoiceResponse]:
    rows = await CollectiveInvoiceService(session).list_members()
    return [CollectiveInvoiceResponse.model_validate(row) for row in rows]


@router.post("", response_model=CollectiveInvoiceResponse, status_code=status.HTTP_201_CREATED)
async def create_collective_invoice(
    body: CollectiveInvoiceCreate,
    _authz: None = Depends(require_permission("can_manage_collective_invoices", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CollectiveInvoiceResponse:
    invoice = await SalesInvoiceService(session).get_invoice(body.sales_invoice_id)
    extra_id = require_collective_extra_shipment(invoice.shipment_id, body.shipment_id)
    anchor = await ShipmentService(session).get_shipment(invoice.shipment_id)
    extra = await ShipmentService(session).get_shipment(extra_id)
    require_collective_same_party(anchor.party_id, extra.party_id)
    row = await CollectiveInvoiceService(session).record_member(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        sales_invoice_id=invoice.id,
        shipment_id=extra.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return CollectiveInvoiceResponse.model_validate(row)
