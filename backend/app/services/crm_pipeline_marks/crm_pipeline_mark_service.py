from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.crm_pipeline_mark import parse_crm_pipeline_mark_row
from app.models.crm_pipeline_mark import CrmPipelineMark
from app.repositories.crm_pipeline_marks.crm_pipeline_mark_repository import (
    CrmPipelineMarkRepository,
)


class CrmPipelineMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CrmPipelineMarkRepository(session)

    async def list_marks(self) -> list[CrmPipelineMark]:
        return await self._rows.list_marks()

    async def persist_crm_pipeline_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        pipeline_kind: object,
        source_ref: object,
    ) -> CrmPipelineMark:
        code, kind, origin = parse_crm_pipeline_mark_row(
            mark_code,
            pipeline_kind,
            source_ref,
        )
        row = CrmPipelineMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            pipeline_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
