from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role_view_mark import RoleViewMark


def _role_view_catalog_query() -> Select[tuple[RoleViewMark]]:
    return select(RoleViewMark).order_by(
        RoleViewMark.mark_code.asc(),
        RoleViewMark.created_at.desc(),
    )


class RoleViewMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RoleViewMark]:
        loaded = await self._session.scalars(_role_view_catalog_query())
        batch: Sequence[RoleViewMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: RoleViewMark) -> RoleViewMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
