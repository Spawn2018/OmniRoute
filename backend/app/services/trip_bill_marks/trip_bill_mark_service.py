from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.trip_bill_mark import parse_trip_bill_mark_row
from app.models.trip_bill_mark import TripBillMark
from app.repositories.trip_bill_marks.trip_bill_mark_repository import (
    TripBillMarkRepository,
)


class TripBillMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TripBillMarkRepository(session)

    async def list_marks(self) -> list[TripBillMark]:
        return await self._rows.list_marks()

    async def persist_trip_bill_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        bill_kind: object,
        source_ref: object,
    ) -> TripBillMark:
        code, kind, origin = parse_trip_bill_mark_row(
            mark_code,
            bill_kind,
            source_ref,
        )
        row = TripBillMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            bill_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
