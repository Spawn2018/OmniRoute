from sqlalchemy.ext.asyncio import AsyncSession

from app.models.version_window import VersionWindow
from app.repositories.version_windows.version_window_repository import (
    VersionWindowRepository,
)


class VersionWindowService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = VersionWindowRepository(session)

    async def list_rows(self) -> list[VersionWindow]:
        return await self._rows.list_rows()
