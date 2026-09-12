from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.freight_term_mark import parse_freight_term_mark_row
from app.models.freight_term_mark import FreightTermMark
from app.repositories.freight_term_marks.freight_term_mark_repository import (
    FreightTermMarkRepository,
)


class FreightTermMarkService:
    """HITL katalog freight term — bez kolumny na shipment i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = FreightTermMarkRepository(session)

    async def list_marks(self) -> list[FreightTermMark]:
        return await self._marks.list_marks()

    async def persist_freight_term_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        term_kind: object,
        source_ref: object,
    ) -> FreightTermMark:
        code, kind, pointer = parse_freight_term_mark_row(
            mark_code,
            term_kind,
            source_ref,
        )
        row = FreightTermMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            term_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
