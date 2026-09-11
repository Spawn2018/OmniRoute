from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.time_to_fix_mark import parse_time_to_fix_mark_row
from app.models.time_to_fix_mark import TimeToFixMark
from app.repositories.time_to_fix_marks.time_to_fix_mark_repository import (
    TimeToFixMarkRepository,
)


class TimeToFixMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TimeToFixMarkRepository(session)

    async def list_marks(self) -> list[TimeToFixMark]:
        return await self._rows.list_marks()

    async def persist_time_to_fix_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        fix_kind: object,
        source_ref: object,
    ) -> TimeToFixMark:
        code, kind, origin = parse_time_to_fix_mark_row(
            mark_code,
            fix_kind,
            source_ref,
        )
        row = TimeToFixMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            fix_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
