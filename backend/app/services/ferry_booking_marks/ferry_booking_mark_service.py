from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ferry_booking_mark import parse_ferry_booking_mark_row
from app.models.ferry_booking_mark import FerryBookingMark
from app.repositories.ferry_booking_marks.ferry_booking_mark_repository import (
    FerryBookingMarkRepository,
)


class FerryBookingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FerryBookingMarkRepository(session)

    async def list_marks(self) -> list[FerryBookingMark]:
        return await self._rows.list_marks()

    async def persist_ferry_booking_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        booking_kind: object,
        source_ref: object,
    ) -> FerryBookingMark:
        code, kind, origin = parse_ferry_booking_mark_row(
            mark_code,
            booking_kind,
            source_ref,
        )
        row = FerryBookingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            booking_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
