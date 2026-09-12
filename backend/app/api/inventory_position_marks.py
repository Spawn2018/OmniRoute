from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.inventory_position_mark import InventoryPositionMark
from app.services.inventory_position_marks.inventory_position_mark_service import (
    InventoryPositionMarkService,
)

router = APIRouter(prefix="/inventory-position-marks", tags=["inventory-position-marks"])

_PERM = "can_manage_inventory_position_marks"


class InventoryPositionMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    stock_kind: str
    source_ref: str


class InventoryPositionMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    stock_kind: str
    source_ref: str


def _row(saved: InventoryPositionMark) -> InventoryPositionMarkResponse:
    return InventoryPositionMarkResponse.model_validate(saved)


@router.get("", response_model=list[InventoryPositionMarkResponse])
async def list_inventory_position_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InventoryPositionMarkResponse]:
    packed = await InventoryPositionMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InventoryPositionMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_position_mark(
    body: InventoryPositionMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InventoryPositionMarkResponse:
    saved = await InventoryPositionMarkService(session).persist_inventory_position_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        stock_kind=body.stock_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
