from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cutoff_mark import parse_cutoff_mark_row
from app.models.cutoff_mark import CutoffMark
from app.repositories.cutoff_marks.cutoff_mark_repository import (
    CutoffMarkRepository,
)


class CutoffMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CutoffMarkRepository(session)

    async def list_marks(self) -> list[CutoffMark]:
        return await self._rows.list_marks()

    async def persist_cutoff_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cutoff_kind: object,
        source_ref: object,
    ) -> CutoffMark:
        code, kind, origin = parse_cutoff_mark_row(
            mark_code,
            cutoff_kind,
            source_ref,
        )
        row = CutoffMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cutoff_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
