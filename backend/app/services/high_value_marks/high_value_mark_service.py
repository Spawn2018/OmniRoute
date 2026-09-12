from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.high_value_mark import parse_high_value_mark_row
from app.models.high_value_mark import HighValueMark
from app.repositories.high_value_marks.high_value_mark_repository import (
    HighValueMarkRepository,
)


class HighValueMarkService:
    """HITL katalog protokołu high-value — bez kolumny shipment i bez cargo_value."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = HighValueMarkRepository(session)

    async def list_marks(self) -> list[HighValueMark]:
        return await self._marks.list_marks()

    async def persist_high_value_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        protocol_kind: object,
        source_ref: object,
    ) -> HighValueMark:
        code, kind, pointer = parse_high_value_mark_row(
            mark_code,
            protocol_kind,
            source_ref,
        )
        row = HighValueMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            protocol_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
