from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_metric_mark import JobMetricMark


def _job_metric_catalog_query() -> Select[tuple[JobMetricMark]]:
    return select(JobMetricMark).order_by(
        JobMetricMark.mark_code.asc(),
        JobMetricMark.created_at.desc(),
    )


class JobMetricMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[JobMetricMark]:
        loaded = await self._session.scalars(_job_metric_catalog_query())
        batch: Sequence[JobMetricMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: JobMetricMark) -> JobMetricMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
