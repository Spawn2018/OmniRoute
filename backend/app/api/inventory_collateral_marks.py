from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.inventory_collateral_mark import InventoryCollateralMark
from app.services.inventory_collateral_marks.inventory_collateral_mark_service import (
    InventoryCollateralMarkService,
)

router = APIRouter(
    prefix="/inventory-collateral-marks",
    tags=["inventory-collateral-marks"],
)

_PERM = "can_manage_inventory_collateral_marks"


class InventoryCollateralMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    collateral_kind: str
    source_ref: str


class InventoryCollateralMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    collateral_kind: str
    source_ref: str


def _row(saved: InventoryCollateralMark) -> InventoryCollateralMarkResponse:
    return InventoryCollateralMarkResponse.model_validate(saved)


@router.get("", response_model=list[InventoryCollateralMarkResponse])
async def list_inventory_collateral_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InventoryCollateralMarkResponse]:
    packed = await InventoryCollateralMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InventoryCollateralMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_collateral_mark(
    body: InventoryCollateralMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InventoryCollateralMarkResponse:
    saved = await InventoryCollateralMarkService(
        session,
    ).persist_inventory_collateral_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        collateral_kind=body.collateral_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
