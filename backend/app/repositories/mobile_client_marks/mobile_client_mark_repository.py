from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mobile_client_mark import MobileClientMark


def _mobile_client_catalog_query() -> Select[tuple[MobileClientMark]]:
    return select(MobileClientMark).order_by(
        MobileClientMark.mark_code.asc(),
        MobileClientMark.created_at.desc(),
    )


class MobileClientMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[MobileClientMark]:
        loaded = await self._session.scalars(_mobile_client_catalog_query())
        batch: Sequence[MobileClientMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: MobileClientMark) -> MobileClientMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
