from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.position_event import PositionEvent
from app.services.position_events.position_event_service import PositionEventService

router = APIRouter(prefix="/position-events", tags=["position-events"])

_PERM = "can_manage_position_events"


class PositionEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_code: str
    source_kind: str
    source_ref: str


class PositionEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    event_code: str
    source_kind: str
    source_ref: str


def _row(saved: PositionEvent) -> PositionEventResponse:
    return PositionEventResponse.model_validate(saved)


@router.get("", response_model=list[PositionEventResponse])
async def list_position_events(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PositionEventResponse]:
    packed = await PositionEventService(session).list_events()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=PositionEventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_position_event(
    body: PositionEventCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PositionEventResponse:
    saved = await PositionEventService(session).persist_position_event(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        event_code=body.event_code,
        source_kind=body.source_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
