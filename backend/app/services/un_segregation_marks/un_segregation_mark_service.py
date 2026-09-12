from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.un_segregation_mark import parse_un_segregation_mark_row
from app.models.un_segregation_mark import UnSegregationMark
from app.repositories.un_segregation_marks.un_segregation_mark_repository import (
    UnSegregationMarkRepository,
)


class UnSegregationMarkService:
    """HITL katalog segregacji UN — bez solver OR i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = UnSegregationMarkRepository(session)

    async def list_marks(self) -> list[UnSegregationMark]:
        return await self._marks.list_marks()

    async def persist_un_segregation_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        segregate_kind: object,
        source_ref: object,
    ) -> UnSegregationMark:
        code, kind, pointer = parse_un_segregation_mark_row(
            mark_code,
            segregate_kind,
            source_ref,
        )
        row = UnSegregationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            segregate_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
