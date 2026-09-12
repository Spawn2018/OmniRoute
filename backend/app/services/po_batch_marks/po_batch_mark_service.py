from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.po_batch_mark import parse_po_batch_mark_row
from app.models.po_batch_mark import PoBatchMark
from app.repositories.po_batch_marks.po_batch_mark_repository import (
    PoBatchMarkRepository,
)


class PoBatchMarkService:
    """HITL katalog po batch — bez live EDI i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = PoBatchMarkRepository(session)

    async def list_marks(self) -> list[PoBatchMark]:
        return await self._marks.list_marks()

    async def persist_po_batch_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        batch_kind: object,
        source_ref: object,
    ) -> PoBatchMark:
        code, kind, pointer = parse_po_batch_mark_row(
            mark_code,
            batch_kind,
            source_ref,
        )
        row = PoBatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            batch_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
