from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.e_doreczenia_mark import parse_e_doreczenia_mark_row
from app.models.e_doreczenia_mark import EDoreczeniaMark
from app.repositories.e_doreczenia_marks.e_doreczenia_mark_repository import (
    EDoreczeniaMarkRepository,
)


class EDoreczeniaMarkService:
    """HITL katalog e-Doręczenia — bez live ADE i bez bajtów PDF."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = EDoreczeniaMarkRepository(session)

    async def list_marks(self) -> list[EDoreczeniaMark]:
        return await self._marks.list_marks()

    async def persist_e_doreczenia_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        delivery_kind: object,
        source_ref: object,
    ) -> EDoreczeniaMark:
        code, kind, pointer = parse_e_doreczenia_mark_row(
            mark_code,
            delivery_kind,
            source_ref,
        )
        row = EDoreczeniaMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            delivery_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
