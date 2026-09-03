from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.outbox_events.outbox_event_service import OutboxEventService

router = APIRouter(prefix="/outbox-events", tags=["outbox-events"])

_AUTHZ = require_permission("can_manage_outbox_events", "organization")


class OutboxEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_id: UUID
    source_ref: str


class OutboxEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    event_kind: str
    subject_id: UUID
    status: str
    source_ref: str


@router.get("", response_model=list[OutboxEventResponse])
async def list_outbox_events(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OutboxEventResponse]:
    rows = await OutboxEventService(session).list_events()
    return [OutboxEventResponse.model_validate(row) for row in rows]


@router.post("", response_model=OutboxEventResponse, status_code=status.HTTP_200_OK)
async def create_outbox_event(
    body: OutboxEventCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OutboxEventResponse:
    row = await OutboxEventService(session).record_message_saved(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_id=body.subject_id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return OutboxEventResponse.model_validate(row)
