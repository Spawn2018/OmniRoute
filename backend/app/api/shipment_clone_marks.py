from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipment_clone_mark import ShipmentCloneMark
from app.services.shipment_clone_marks.shipment_clone_mark_service import (
    ShipmentCloneMarkService,
)

router = APIRouter(
    prefix="/shipment-clone-marks",
    tags=["shipment-clone-marks"],
)

_PERM = "can_manage_shipment_clone_marks"


class ShipmentCloneMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    clone_kind: str
    source_ref: str


class ShipmentCloneMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    clone_kind: str
    source_ref: str


def _row(saved: ShipmentCloneMark) -> ShipmentCloneMarkResponse:
    return ShipmentCloneMarkResponse.model_validate(saved)


@router.get("", response_model=list[ShipmentCloneMarkResponse])
async def list_shipment_clone_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipmentCloneMarkResponse]:
    packed = await ShipmentCloneMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ShipmentCloneMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipment_clone_mark(
    body: ShipmentCloneMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipmentCloneMarkResponse:
    saved = await ShipmentCloneMarkService(session).persist_shipment_clone_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        clone_kind=body.clone_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
