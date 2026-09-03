from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.bookkeeping.bookkeeping_service import BookkeepingService
from app.services.charges.charge_service import ChargeService
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService

router = APIRouter(prefix="/bookkeepings", tags=["bookkeepings"])


class BookkeepingCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    charge_id: UUID
    sales_invoice_id: UUID
    source_ref: str


class BookkeepingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    charge_id: UUID
    sales_invoice_id: UUID
    source_ref: str


@router.get("", response_model=list[BookkeepingResponse])
async def list_bookkeeping(
    _authz: None = Depends(require_permission("can_manage_bookkeeping", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[BookkeepingResponse]:
    rows = await BookkeepingService(session).list_entries()
    return [BookkeepingResponse.model_validate(row) for row in rows]


@router.post("", response_model=BookkeepingResponse, status_code=status.HTTP_201_CREATED)
async def create_bookkeeping(
    body: BookkeepingCreate,
    _authz: None = Depends(require_permission("can_manage_bookkeeping", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> BookkeepingResponse:
    charge = await ChargeService(session).get_charge(body.charge_id)
    invoice = await SalesInvoiceService(session).get_invoice(body.sales_invoice_id)
    row = await BookkeepingService(session).record_entry(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        charge_id=charge.id,
        sales_invoice_id=invoice.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return BookkeepingResponse.model_validate(row)
