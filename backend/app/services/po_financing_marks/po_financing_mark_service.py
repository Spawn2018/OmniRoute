from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.po_financing_mark import parse_po_financing_mark_row
from app.models.po_financing_mark import PoFinancingMark
from app.repositories.po_financing_marks.po_financing_mark_repository import (
    PoFinancingMarkRepository,
)


class PoFinancingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PoFinancingMarkRepository(session)

    async def list_marks(self) -> list[PoFinancingMark]:
        return await self._rows.list_marks()

    async def persist_po_financing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        financing_kind: object,
        source_ref: object,
    ) -> PoFinancingMark:
        code, kind, origin = parse_po_financing_mark_row(
            mark_code,
            financing_kind,
            source_ref,
        )
        row = PoFinancingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            financing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
