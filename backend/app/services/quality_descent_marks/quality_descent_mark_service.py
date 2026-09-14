from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.quality_descent_mark import parse_quality_descent_mark_row
from app.models.quality_descent_mark import QualityDescentMark
from app.repositories.quality_descent_marks.quality_descent_mark_repository import (
    QualityDescentMarkRepository,
)


class QualityDescentMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = QualityDescentMarkRepository(session)

    async def list_marks(self) -> list[QualityDescentMark]:
        return await self._rows.list_marks()

    async def persist_quality_descent_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        descent_kind: object,
        source_ref: object,
    ) -> QualityDescentMark:
        code, kind, origin = parse_quality_descent_mark_row(
            mark_code,
            descent_kind,
            source_ref,
        )
        row = QualityDescentMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            descent_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
