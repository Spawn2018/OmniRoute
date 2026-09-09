from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.war_room_mark import WarRoomMark
from app.services.war_room_marks.war_room_mark_service import WarRoomMarkService

router = APIRouter(prefix="/war-room-marks", tags=["war-room-marks"])

_PERM = "can_manage_war_room_marks"


class WarRoomMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    incident_kind: str
    source_ref: str


class WarRoomMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    incident_kind: str
    source_ref: str


def _as_row(row: WarRoomMark) -> WarRoomMarkResponse:
    return WarRoomMarkResponse.model_validate(row)


@router.get("", response_model=list[WarRoomMarkResponse])
async def list_war_room_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WarRoomMarkResponse]:
    rows = await WarRoomMarkService(session).list_incidents()
    return [_as_row(row) for row in rows]


@router.post("", response_model=WarRoomMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_war_room_mark(
    body: WarRoomMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WarRoomMarkResponse:
    row = await WarRoomMarkService(session).record_incident(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        incident_kind=body.incident_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
