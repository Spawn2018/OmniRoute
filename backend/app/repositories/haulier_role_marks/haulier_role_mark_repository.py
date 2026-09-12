from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.haulier_role_mark import HaulierRoleMark


def _haulier_role_catalog_query() -> Select[tuple[HaulierRoleMark]]:
    return select(HaulierRoleMark).order_by(
        HaulierRoleMark.mark_code.asc(),
        HaulierRoleMark.created_at.desc(),
    )


class HaulierRoleMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[HaulierRoleMark]:
        loaded = await self._session.scalars(_haulier_role_catalog_query())
        batch: Sequence[HaulierRoleMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: HaulierRoleMark) -> HaulierRoleMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
