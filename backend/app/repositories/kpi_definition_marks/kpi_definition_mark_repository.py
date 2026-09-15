from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.kpi_definition_mark import KpiDefinitionMark


class KpiDefinitionMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[KpiDefinitionMark]:
        stmt = select(KpiDefinitionMark).order_by(
            KpiDefinitionMark.mark_code,
            KpiDefinitionMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: KpiDefinitionMark) -> KpiDefinitionMark:
        self._session.add(row)
        await self._session.flush()
        return row
