from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.waste_mark import parse_waste_mark_row
from app.models.waste_mark import WasteMark
from app.repositories.waste_marks import WasteMarkRepository


class WasteMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = WasteMarkRepository(session)

    async def list_marks(self) -> list[WasteMark]:
        return await self._rows.list_marks()

    async def persist_waste_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        waste_kind: object,
        source_ref: object,
    ) -> WasteMark:
        code, kind, origin = parse_waste_mark_row(mark_code, waste_kind, source_ref)
        row = WasteMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            waste_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
