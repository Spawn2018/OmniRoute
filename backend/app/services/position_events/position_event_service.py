from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.position_event import parse_position_event_row
from app.models.position_event import PositionEvent
from app.repositories.position_events.position_event_repository import (
    PositionEventRepository,
)


class PositionEventService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PositionEventRepository(session)

    async def list_events(self) -> list[PositionEvent]:
        return await self._rows.list_events()

    async def persist_position_event(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        event_code: object,
        source_kind: object,
        source_ref: object,
    ) -> PositionEvent:
        code, kind, origin = parse_position_event_row(
            event_code,
            source_kind,
            source_ref,
        )
        row = PositionEvent(
            id=uuid4(),
            organization_id=organization_id,
            event_code=code,
            source_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_event(row)
