from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.silk_corridor_mark import parse_silk_corridor_mark_row
from app.models.silk_corridor_mark import SilkCorridorMark
from app.repositories.silk_corridor_marks.silk_corridor_mark_repository import (
    SilkCorridorMarkRepository,
)


class SilkCorridorMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SilkCorridorMarkRepository(session)

    async def list_marks(self) -> list[SilkCorridorMark]:
        return await self._rows.list_marks()

    async def persist_silk_corridor_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        corridor_kind: object,
        source_ref: object,
    ) -> SilkCorridorMark:
        code, kind, origin = parse_silk_corridor_mark_row(
            mark_code,
            corridor_kind,
            source_ref,
        )
        row = SilkCorridorMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            corridor_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
