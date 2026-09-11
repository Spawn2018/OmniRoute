from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.po_line import PoLine
from app.services.purchase_orders.po_line_service import PoLineService

router = APIRouter(prefix="/po-lines", tags=["po-lines"])

_PERM = "can_manage_purchase_orders"


class PoLineCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    purchase_order_id: UUID
    line_code: str
    sku_code: str
    qty: str | int | float | bool
    uom_code: str
    plant_label: str | None = None
    batch_label: str | None = None
    serial_label: str | None = None
    coo_label: str | None = None
    source_ref: str


class PoLineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    purchase_order_id: UUID
    line_code: str
    sku_code: str
    qty: str
    uom_code: str
    plant_label: str | None
    batch_label: str | None
    serial_label: str | None
    coo_label: str | None
    source_ref: str


def _line(saved: PoLine) -> PoLineResponse:
    return PoLineResponse(
        id=saved.id,
        organization_id=saved.organization_id,
        purchase_order_id=saved.purchase_order_id,
        line_code=saved.line_code,
        sku_code=saved.sku_code,
        qty=format(saved.qty, "f"),
        uom_code=saved.uom_code,
        plant_label=saved.plant_label,
        batch_label=saved.batch_label,
        serial_label=saved.serial_label,
        coo_label=saved.coo_label,
        source_ref=saved.source_ref,
    )


@router.get("", response_model=list[PoLineResponse])
async def list_po_lines(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PoLineResponse]:
    packed = await PoLineService(session).list_lines()
    return [_line(item) for item in packed]


@router.post("", response_model=PoLineResponse, status_code=status.HTTP_201_CREATED)
async def create_po_line(
    body: PoLineCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PoLineResponse:
    saved = await PoLineService(session).persist_po_line(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        purchase_order_id=body.purchase_order_id,
        line_code=body.line_code,
        sku_code=body.sku_code,
        qty=body.qty,
        uom_code=body.uom_code,
        plant_label=body.plant_label,
        batch_label=body.batch_label,
        serial_label=body.serial_label,
        coo_label=body.coo_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _line(saved)
