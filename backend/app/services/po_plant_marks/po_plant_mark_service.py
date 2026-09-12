from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.po_plant_mark import parse_po_plant_mark_row
from app.models.po_plant_mark import PoPlantMark
from app.repositories.po_plant_marks.po_plant_mark_repository import (
    PoPlantMarkRepository,
)


class PoPlantMarkService:
    """HITL katalog po plant — bez live EDI i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = PoPlantMarkRepository(session)

    async def list_marks(self) -> list[PoPlantMark]:
        return await self._marks.list_marks()

    async def persist_po_plant_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        plant_kind: object,
        source_ref: object,
    ) -> PoPlantMark:
        code, kind, pointer = parse_po_plant_mark_row(
            mark_code,
            plant_kind,
            source_ref,
        )
        row = PoPlantMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            plant_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
