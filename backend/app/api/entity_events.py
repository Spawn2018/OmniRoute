from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.entity_events.entity_event_service import EntityEventService

router = APIRouter(prefix="/entity-events", tags=["entity-events"])

_AUTHZ = require_permission("can_manage_entity_events", "organization")


class EntityEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    subject_kind: str
    subject_id: UUID
    event_kind: str
    source_ref: str
    occurred_at: datetime | None = None


class EntityEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    subject_kind: str
    subject_id: UUID
    event_kind: str
    occurred_at: datetime
    source_ref: str


@router.get("", response_model=list[EntityEventResponse])
async def list_entity_events(
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[EntityEventResponse]:
    rows = await EntityEventService(session).list_events()
    return [EntityEventResponse.model_validate(row) for row in rows]


@router.post("", response_model=EntityEventResponse, status_code=status.HTTP_200_OK)
async def create_entity_event(
    body: EntityEventCreate,
    _authz: None = Depends(_AUTHZ),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> EntityEventResponse:
    row = await EntityEventService(session).create_event(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        subject_kind=body.subject_kind,
        subject_id=body.subject_id,
        event_kind=body.event_kind,
        source_ref=body.source_ref,
        occurred_at=body.occurred_at,
    )
    await session.commit()
    return EntityEventResponse.model_validate(row)
