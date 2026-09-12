from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.job_metric_mark import parse_job_metric_mark_row
from app.models.job_metric_mark import JobMetricMark
from app.repositories.job_metric_marks.job_metric_mark_repository import (
    JobMetricMarkRepository,
)


class JobMetricMarkService:
    """HITL katalog metryki jobu — bez scoringu osoby i bez SQL job."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = JobMetricMarkRepository(session)

    async def list_marks(self) -> list[JobMetricMark]:
        return await self._marks.list_marks()

    async def persist_job_metric_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        metric_kind: object,
        source_ref: object,
    ) -> JobMetricMark:
        code, kind, pointer = parse_job_metric_mark_row(
            mark_code,
            metric_kind,
            source_ref,
        )
        row = JobMetricMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            metric_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
