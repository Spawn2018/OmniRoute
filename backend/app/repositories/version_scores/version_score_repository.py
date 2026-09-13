from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.version_score import VersionScore


def _version_score_query() -> Select[tuple[VersionScore]]:
    return select(VersionScore).order_by(VersionScore.avg_crps, VersionScore.model_version)


class VersionScoreRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[VersionScore]:
        loaded = await self._session.scalars(_version_score_query())
        batch: Sequence[VersionScore] = loaded.all()
        return list(batch)
