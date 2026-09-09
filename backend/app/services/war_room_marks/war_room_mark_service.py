from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.war_room_mark import require_incident_kind, require_room_source_ref
from app.models.war_room_mark import WarRoomMark
from app.repositories.war_room_marks.war_room_mark_repository import (
    WarRoomMarkRepository,
)


class WarRoomMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._incidents = WarRoomMarkRepository(session)

    async def list_incidents(self) -> list[WarRoomMark]:
        return await self._incidents.fetch_incidents()

    async def record_incident(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        incident_kind: object,
        source_ref: object,
    ) -> WarRoomMark:
        kind = require_incident_kind(incident_kind)
        origin = require_room_source_ref(source_ref)
        packed = WarRoomMark(
            id=uuid4(),
            organization_id=organization_id,
            incident_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._incidents.add(packed)
