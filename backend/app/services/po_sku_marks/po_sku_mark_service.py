from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.po_sku_mark import parse_po_sku_mark_row
from app.models.po_sku_mark import PoSkuMark
from app.repositories.po_sku_marks.po_sku_mark_repository import (
    PoSkuMarkRepository,
)


class PoSkuMarkService:
    """HITL katalog po sku — bez live EDI i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = PoSkuMarkRepository(session)

    async def list_marks(self) -> list[PoSkuMark]:
        return await self._marks.list_marks()

    async def persist_po_sku_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sku_kind: object,
        source_ref: object,
    ) -> PoSkuMark:
        code, kind, pointer = parse_po_sku_mark_row(
            mark_code,
            sku_kind,
            source_ref,
        )
        row = PoSkuMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sku_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
