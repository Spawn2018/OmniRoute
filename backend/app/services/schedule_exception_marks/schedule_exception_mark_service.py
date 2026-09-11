from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schedule_exception_mark import parse_schedule_exception_mark_row
from app.models.schedule_exception_mark import ScheduleExceptionMark
from app.repositories.schedule_exception_marks.schedule_exception_mark_repository import (
    ScheduleExceptionMarkRepository,
)


class ScheduleExceptionMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ScheduleExceptionMarkRepository(session)

    async def list_marks(self) -> list[ScheduleExceptionMark]:
        return await self._rows.list_marks()

    async def persist_schedule_exception_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        exception_kind: object,
        source_ref: object,
    ) -> ScheduleExceptionMark:
        code, kind, origin = parse_schedule_exception_mark_row(
            mark_code,
            exception_kind,
            source_ref,
        )
        row = ScheduleExceptionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            exception_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
