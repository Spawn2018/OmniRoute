from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.executive_mark import require_brief_source_ref, require_question_kind
from app.models.executive_mark import ExecutiveMark
from app.repositories.executive_marks.executive_mark_repository import (
    ExecutiveMarkRepository,
)


class ExecutiveMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._briefs = ExecutiveMarkRepository(session)

    async def list_briefs(self) -> list[ExecutiveMark]:
        return await self._briefs.fetch_briefs()

    async def record_brief(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        question_kind: object,
        source_ref: object,
    ) -> ExecutiveMark:
        kind = require_question_kind(question_kind)
        origin = require_brief_source_ref(source_ref)
        packed = ExecutiveMark(
            id=uuid4(),
            organization_id=organization_id,
            question_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._briefs.add(packed)
