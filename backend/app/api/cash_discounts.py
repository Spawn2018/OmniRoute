from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cash_discount import CashDiscount
from app.services.cash_discounts.cash_discount_service import CashDiscountService
from app.services.sales_invoices.sales_invoice_service import SalesInvoiceService

router = APIRouter(prefix="/cash-discounts", tags=["cash-discounts"])

_PERM = "can_manage_cash_discounts"


class CashDiscountCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sales_invoice_id: UUID
    discount_kind: str
    source_ref: str


class CashDiscountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    sales_invoice_id: UUID
    discount_kind: str
    source_ref: str


def _as_row(row: CashDiscount) -> CashDiscountResponse:
    return CashDiscountResponse(
        id=row.id,
        organization_id=row.organization_id,
        sales_invoice_id=row.sales_invoice_id,
        discount_kind=row.discount_kind,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[CashDiscountResponse])
async def list_cash_discounts(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CashDiscountResponse]:
    rows = await CashDiscountService(session).list_discounts()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=CashDiscountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cash_discount(
    body: CashDiscountCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CashDiscountResponse:
    invoice = await SalesInvoiceService(session).get_invoice(body.sales_invoice_id)
    row = await CashDiscountService(session).persist_discount(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        sales_invoice_id=invoice.id,
        discount_kind=body.discount_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
