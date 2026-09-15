from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cfo_narrative_mark import parse_cfo_narrative_mark_row
from app.models.cfo_narrative_mark import CfoNarrativeMark
from app.repositories.cfo_narrative_marks.cfo_narrative_mark_repository import (
    CfoNarrativeMarkRepository,
)


class CfoNarrativeMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CfoNarrativeMarkRepository(session)

    async def list_marks(self) -> list[CfoNarrativeMark]:
        return await self._rows.list_marks()

    async def persist_cfo_narrative_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        narrative_kind: object,
        source_ref: object,
    ) -> CfoNarrativeMark:
        code, kind, origin = parse_cfo_narrative_mark_row(
            mark_code,
            narrative_kind,
            source_ref,
        )
        row = CfoNarrativeMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            narrative_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
