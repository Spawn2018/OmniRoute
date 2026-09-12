from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.three_way_mark import parse_three_way_mark_row
from app.models.three_way_mark import ThreeWayMark
from app.repositories.three_way_marks.three_way_mark_repository import (
    ThreeWayMarkRepository,
)


class ThreeWayMarkService:
    """HITL katalog 3-way — bez tuple per strona i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ThreeWayMarkRepository(session)

    async def list_marks(self) -> list[ThreeWayMark]:
        return await self._marks.list_marks()

    async def persist_three_way_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        way_kind: object,
        source_ref: object,
    ) -> ThreeWayMark:
        code, kind, pointer = parse_three_way_mark_row(
            mark_code,
            way_kind,
            source_ref,
        )
        row = ThreeWayMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            way_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
