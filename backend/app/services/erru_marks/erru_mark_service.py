from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.erru_mark import parse_erru_mark_row
from app.models.erru_mark import ErruMark
from app.repositories.erru_marks.erru_mark_repository import (
    ErruMarkRepository,
)


class ErruMarkService:
    """HITL katalog sprawdzenia ERRU — bez live ERRU i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ErruMarkRepository(session)

    async def list_marks(self) -> list[ErruMark]:
        return await self._marks.list_marks()

    async def persist_erru_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        check_kind: object,
        source_ref: object,
    ) -> ErruMark:
        code, kind, pointer = parse_erru_mark_row(
            mark_code,
            check_kind,
            source_ref,
        )
        row = ErruMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            check_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
