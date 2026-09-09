from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.free_time_clock import (
    require_clock_kind,
    require_clock_source_ref,
    require_free_days,
)
from app.models.free_time_clock import FreeTimeClock
from app.repositories.free_time_clocks.free_time_clock_repository import FreeTimeClockRepository


class FreeTimeClockService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = FreeTimeClockRepository(session)

    async def list_marks(self) -> list[FreeTimeClock]:
        return await self._marks.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        clock_kind: object,
        free_days: object,
        source_ref: object,
    ) -> FreeTimeClock:
        row = FreeTimeClock(
            id=uuid4(),
            organization_id=organization_id,
            clock_kind=require_clock_kind(clock_kind),
            free_days=require_free_days(free_days),
            source_ref=require_clock_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.add(row)
