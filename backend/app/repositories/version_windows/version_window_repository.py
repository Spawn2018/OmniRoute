from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.version_window import VersionWindow


def _version_window_query() -> Select[tuple[VersionWindow]]:
    return select(VersionWindow).order_by(
        VersionWindow.created_on.desc(),
        VersionWindow.avg_crps,
        VersionWindow.model_version,
    )


class VersionWindowRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[VersionWindow]:
        loaded = await self._session.scalars(_version_window_query())
        batch: Sequence[VersionWindow] = loaded.all()
        return list(batch)
