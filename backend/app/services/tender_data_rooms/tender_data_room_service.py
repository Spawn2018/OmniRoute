from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_data_room import require_board_id, require_nda_mark, require_room_source_ref
from app.models.tender_data_room import TenderDataRoom
from app.repositories.tender_data_rooms.tender_data_room_repository import TenderDataRoomRepository


class TenderDataRoomService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TenderDataRoomRepository(session)

    async def list_rooms(self) -> list[TenderDataRoom]:
        return await self._rows.fetch_rows()

    async def record_room(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        nda_mark: object,
        source_ref: object,
    ) -> TenderDataRoom:
        row = TenderDataRoom(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            nda_mark=require_nda_mark(nda_mark),
            source_ref=require_room_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
