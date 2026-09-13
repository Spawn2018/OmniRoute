from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interval_score import IntervalScore
from app.repositories.interval_scores.interval_score_repository import (
    IntervalScoreRepository,
)


class IntervalScoreService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = IntervalScoreRepository(session)

    async def list_rows(self) -> list[IntervalScore]:
        return await self._rows.list_rows()
