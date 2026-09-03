from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.shipments.shipment_service import ShipmentService
from app.services.tracking_events.tracking_event_service import TrackingEventService

router = APIRouter(prefix="/tracking-events", tags=["tracking-events"])


class TrackingEventCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shipment_id: UUID
    event_kind: str
    occurred_at: datetime
    source_ref: str


class TrackingEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    shipment_id: UUID
    event_kind: str
    occurred_at: datetime
    source_ref: str


@router.get("", response_model=list[TrackingEventResponse])
async def list_tracking_events(
    _authz: None = Depends(require_permission("can_manage_tracking", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TrackingEventResponse]:
    rows = await TrackingEventService(session).list_events()
    return [TrackingEventResponse.model_validate(row) for row in rows]


@router.post("", response_model=TrackingEventResponse, status_code=status.HTTP_201_CREATED)
async def create_tracking_event(
    body: TrackingEventCreate,
    _authz: None = Depends(require_permission("can_manage_tracking", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TrackingEventResponse:
    shipment = await ShipmentService(session).get_shipment(body.shipment_id)
    row = await TrackingEventService(session).record_event(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        shipment_id=shipment.id,
        event_kind=body.event_kind,
        occurred_at=body.occurred_at,
        source_ref=body.source_ref,
    )
    await session.commit()
    return TrackingEventResponse.model_validate(row)
