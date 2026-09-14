from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ops_room_mark import OpsRoomMark
from app.services.ops_room_marks.ops_room_mark_service import OpsRoomMarkService

router = APIRouter(
    prefix="/ops-room-marks",
    tags=["ops-room-marks"],
)

_PERM = "can_manage_ops_room_marks"


class OpsRoomMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    layer_kind: str
    source_ref: str


class OpsRoomMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    layer_kind: str
    source_ref: str


def _row(saved: OpsRoomMark) -> OpsRoomMarkResponse:
    return OpsRoomMarkResponse.model_validate(saved)


@router.get("", response_model=list[OpsRoomMarkResponse])
async def list_ops_room_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OpsRoomMarkResponse]:
    packed = await OpsRoomMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=OpsRoomMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ops_room_mark(
    body: OpsRoomMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OpsRoomMarkResponse:
    saved = await OpsRoomMarkService(session).persist_ops_room_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        layer_kind=body.layer_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
