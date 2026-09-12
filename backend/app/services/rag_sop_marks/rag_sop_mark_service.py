from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rag_sop_mark import parse_rag_sop_mark_row
from app.models.rag_sop_mark import RagSopMark
from app.repositories.rag_sop_marks.rag_sop_mark_repository import (
    RagSopMarkRepository,
)


class RagSopMarkService:
    """HITL katalog zakresu RAG — bez pgvector i bez wyceny."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = RagSopMarkRepository(session)

    async def list_marks(self) -> list[RagSopMark]:
        return await self._marks.list_marks()

    async def persist_rag_sop_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        scope_kind: object,
        source_ref: object,
    ) -> RagSopMark:
        code, kind, pointer = parse_rag_sop_mark_row(
            mark_code,
            scope_kind,
            source_ref,
        )
        row = RagSopMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            scope_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
