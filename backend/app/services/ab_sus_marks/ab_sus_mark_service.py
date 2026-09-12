from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ab_sus_mark import parse_ab_sus_mark_row
from app.models.ab_sus_mark import AbSusMark
from app.repositories.ab_sus_marks.ab_sus_mark_repository import (
    AbSusMarkRepository,
)


class AbSusMarkService:
    """HITL katalog A/B+SUS — bez A/B live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = AbSusMarkRepository(session)

    async def list_marks(self) -> list[AbSusMark]:
        return await self._marks.list_marks()

    async def persist_ab_sus_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        trial_kind: object,
        source_ref: object,
    ) -> AbSusMark:
        code, kind, pointer = parse_ab_sus_mark_row(
            mark_code,
            trial_kind,
            source_ref,
        )
        row = AbSusMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            trial_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
