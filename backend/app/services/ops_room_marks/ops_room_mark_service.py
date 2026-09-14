from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ops_room_mark import parse_ops_room_mark_row
from app.models.ops_room_mark import OpsRoomMark
from app.repositories.ops_room_marks.ops_room_mark_repository import (
    OpsRoomMarkRepository,
)


class OpsRoomMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = OpsRoomMarkRepository(session)

    async def list_marks(self) -> list[OpsRoomMark]:
        return await self._rows.list_marks()

    async def persist_ops_room_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        layer_kind: object,
        source_ref: object,
    ) -> OpsRoomMark:
        code, kind, origin = parse_ops_room_mark_row(
            mark_code,
            layer_kind,
            source_ref,
        )
        row = OpsRoomMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            layer_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
