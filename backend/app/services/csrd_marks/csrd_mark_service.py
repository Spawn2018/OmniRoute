from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.csrd_mark import parse_csrd_mark_row
from app.models.csrd_mark import CsrdMark
from app.repositories.csrd_marks.csrd_mark_repository import CsrdMarkRepository


class CsrdMarkService:
    """HITL katalog CSRD — bez kg/tCO2e i bez live filing."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = CsrdMarkRepository(session)

    async def list_marks(self) -> list[CsrdMark]:
        return await self._marks.list_marks()

    async def persist_csrd_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        report_kind: object,
        source_ref: object,
    ) -> CsrdMark:
        code, kind, pointer = parse_csrd_mark_row(mark_code, report_kind, source_ref)
        row = CsrdMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            report_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
