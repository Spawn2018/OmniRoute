from sqlalchemy.ext.asyncio import AsyncSession

from app.models.version_score import VersionScore
from app.repositories.version_scores.version_score_repository import (
    VersionScoreRepository,
)


class VersionScoreService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = VersionScoreRepository(session)

    async def list_rows(self) -> list[VersionScore]:
        return await self._rows.list_rows()
