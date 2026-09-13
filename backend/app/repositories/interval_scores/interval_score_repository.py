from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interval_score import IntervalScore


def _interval_score_query() -> Select[tuple[IntervalScore]]:
    return select(IntervalScore).order_by(IntervalScore.outcome_id)


class IntervalScoreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[IntervalScore]:
        loaded = await self._session.scalars(_interval_score_query())
        batch: Sequence[IntervalScore] = loaded.all()
        return list(batch)
