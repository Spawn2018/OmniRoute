from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tacho_office_mark import TachoOfficeMark


def _tacho_catalog_query() -> Select[tuple[TachoOfficeMark]]:
    return select(TachoOfficeMark).order_by(
        TachoOfficeMark.mark_code.asc(),
        TachoOfficeMark.created_at.desc(),
    )


class TachoOfficeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[TachoOfficeMark]:
        loaded = await self._session.scalars(_tacho_catalog_query())
        batch: Sequence[TachoOfficeMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: TachoOfficeMark) -> TachoOfficeMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
