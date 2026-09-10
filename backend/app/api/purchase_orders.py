from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.purchase_order import PurchaseOrder
from app.services.purchase_orders.purchase_order_service import PurchaseOrderService

router = APIRouter(prefix="/purchase-orders", tags=["purchase-orders"])

_PERM = "can_manage_purchase_orders"


class PurchaseOrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    po_code: str
    plant_label: str | None = None
    source_ref: str


class PurchaseOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    po_code: str
    plant_label: str | None
    source_ref: str


def _header(saved: PurchaseOrder) -> PurchaseOrderResponse:
    return PurchaseOrderResponse.model_validate(saved)


@router.get("", response_model=list[PurchaseOrderResponse])
async def list_purchase_orders(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PurchaseOrderResponse]:
    packed = await PurchaseOrderService(session).list_headers()
    return [_header(item) for item in packed]


@router.post(
    "",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_purchase_order(
    body: PurchaseOrderCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PurchaseOrderResponse:
    saved = await PurchaseOrderService(session).persist_purchase_order(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        po_code=body.po_code,
        plant_label=body.plant_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _header(saved)
