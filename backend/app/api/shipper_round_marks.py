from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.shipper_round_mark import ShipperRoundMark
from app.services.shipper_round_marks.shipper_round_mark_service import (
    ShipperRoundMarkService,
)

router = APIRouter(prefix="/shipper-round-marks", tags=["shipper-round-marks"])

_PERM = "can_manage_shipper_round_marks"


class ShipperRoundMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    round_kind: str
    source_ref: str


class ShipperRoundMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    round_kind: str
    source_ref: str


def _row(saved: ShipperRoundMark) -> ShipperRoundMarkResponse:
    return ShipperRoundMarkResponse.model_validate(saved)


@router.get("", response_model=list[ShipperRoundMarkResponse])
async def list_shipper_round_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ShipperRoundMarkResponse]:
    packed = await ShipperRoundMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ShipperRoundMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_shipper_round_mark(
    body: ShipperRoundMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ShipperRoundMarkResponse:
    saved = await ShipperRoundMarkService(session).persist_shipper_round_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        round_kind=body.round_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
