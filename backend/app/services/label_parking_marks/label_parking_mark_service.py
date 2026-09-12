from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.label_parking_mark import parse_label_parking_mark_row
from app.models.label_parking_mark import LabelParkingMark
from app.repositories.label_parking_marks.label_parking_mark_repository import (
    LabelParkingMarkRepository,
)


class LabelParkingMarkService:
    """HITL katalog LABEL parking — bez parking live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = LabelParkingMarkRepository(session)

    async def list_marks(self) -> list[LabelParkingMark]:
        return await self._marks.list_marks()

    async def persist_label_parking_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        parking_kind: object,
        source_ref: object,
    ) -> LabelParkingMark:
        code, kind, pointer = parse_label_parking_mark_row(
            mark_code,
            parking_kind,
            source_ref,
        )
        row = LabelParkingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            parking_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
