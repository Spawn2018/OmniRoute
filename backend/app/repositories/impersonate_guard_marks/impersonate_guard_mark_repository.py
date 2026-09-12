from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.impersonate_guard_mark import ImpersonateGuardMark


def _impersonate_guard_catalog_query() -> Select[tuple[ImpersonateGuardMark]]:
    return select(ImpersonateGuardMark).order_by(
        ImpersonateGuardMark.mark_code.asc(),
        ImpersonateGuardMark.created_at.desc(),
    )


class ImpersonateGuardMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ImpersonateGuardMark]:
        loaded = await self._session.scalars(_impersonate_guard_catalog_query())
        batch: Sequence[ImpersonateGuardMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: ImpersonateGuardMark) -> ImpersonateGuardMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
