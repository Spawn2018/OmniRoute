from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rfid_mark import parse_rfid_mark_row
from app.models.rfid_mark import RfidMark
from app.repositories.rfid_marks.rfid_mark_repository import RfidMarkRepository


class RfidMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RfidMarkRepository(session)

    async def list_marks(self) -> list[RfidMark]:
        return await self._rows.list_marks()

    async def persist_rfid_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        rfid_kind: object,
        source_ref: object,
    ) -> RfidMark:
        code, kind, origin = parse_rfid_mark_row(mark_code, rfid_kind, source_ref)
        row = RfidMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            rfid_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
