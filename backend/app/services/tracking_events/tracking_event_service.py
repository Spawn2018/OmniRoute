from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tracking_event import (
    require_event_kind,
    require_occurred_at,
    require_shipment_id,
    require_tracking_source_ref,
)
from app.models.tracking_event import TrackingEvent
from app.repositories.tracking_events.tracking_event_repository import TrackingEventRepository


class TrackingEventService:
    def __init__(self, session: AsyncSession) -> None:
        self._events = TrackingEventRepository(session)

    async def list_events(self) -> list[TrackingEvent]:
        return await self._events.list_all()

    async def record_event(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        event_kind: str,
        occurred_at: datetime,
        source_ref: str,
    ) -> TrackingEvent:
        row = TrackingEvent(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_shipment_id(shipment_id),
            event_kind=require_event_kind(event_kind),
            occurred_at=require_occurred_at(occurred_at),
            source_ref=require_tracking_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._events.add(row)
