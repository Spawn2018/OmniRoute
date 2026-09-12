from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.funnel_mark import parse_funnel_mark_row
from app.models.funnel_mark import FunnelMark
from app.repositories.funnel_marks.funnel_mark_repository import (
    FunnelMarkRepository,
)


class FunnelMarkService:
    """HITL katalog X7 lejek — bez funnel live API i bez scrape."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = FunnelMarkRepository(session)

    async def list_marks(self) -> list[FunnelMark]:
        return await self._marks.list_marks()

    async def persist_funnel_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        funnel_kind: object,
        source_ref: object,
    ) -> FunnelMark:
        code, kind, pointer = parse_funnel_mark_row(
            mark_code,
            funnel_kind,
            source_ref,
        )
        row = FunnelMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            funnel_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
