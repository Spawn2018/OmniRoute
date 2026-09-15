from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.crm_pipeline_mark import CrmPipelineMark


class CrmPipelineMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CrmPipelineMark]:
        packed = await self._session.scalars(
            select(CrmPipelineMark).order_by(
                CrmPipelineMark.mark_code,
                CrmPipelineMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CrmPipelineMark) -> CrmPipelineMark:
        self._session.add(row)
        await self._session.flush()
        return row
