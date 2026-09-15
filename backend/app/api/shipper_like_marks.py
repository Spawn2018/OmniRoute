from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipper_like_mark import ShipperLikeMark
from app.services.shipper_like_marks.shipper_like_mark_service import (
    ShipperLikeMarkService,
)

router = APIRouter(prefix="/shipper-like-marks", tags=["shipper-like-marks"])

_PERM = "can_manage_shipper_like_marks"


class ShipperLikeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    like_kind: str
    source_ref: str


class ShipperLikeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    like_kind: str
    source_ref: str


def _row(saved: ShipperLikeMark) -> ShipperLikeMarkResponse:
    return ShipperLikeMarkResponse.model_validate(saved)


@router.get("", response_model=list[ShipperLikeMarkResponse])
async def list_shipper_like_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipperLikeMarkResponse]:
    packed = await ShipperLikeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ShipperLikeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipper_like_mark(
    body: ShipperLikeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipperLikeMarkResponse:
    saved = await ShipperLikeMarkService(session).persist_shipper_like_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        like_kind=body.like_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
