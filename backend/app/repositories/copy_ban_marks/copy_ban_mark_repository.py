from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.copy_ban_mark import CopyBanMark


def _copy_ban_catalog_query() -> Select[tuple[CopyBanMark]]:
    return select(CopyBanMark).order_by(
        CopyBanMark.mark_code.asc(),
        CopyBanMark.created_at.desc(),
    )


class CopyBanMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CopyBanMark]:
        loaded = await self._session.scalars(_copy_ban_catalog_query())
        batch: Sequence[CopyBanMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: CopyBanMark) -> CopyBanMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
