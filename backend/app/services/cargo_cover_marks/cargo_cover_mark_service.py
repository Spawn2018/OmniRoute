from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cargo_cover_mark import parse_cargo_cover_mark_row
from app.models.cargo_cover_mark import CargoCoverMark
from app.repositories.cargo_cover_marks.cargo_cover_mark_repository import (
    CargoCoverMarkRepository,
)


class CargoCoverMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CargoCoverMarkRepository(session)

    async def list_marks(self) -> list[CargoCoverMark]:
        return await self._rows.list_marks()

    async def persist_cargo_cover_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cover_kind: object,
        source_ref: object,
    ) -> CargoCoverMark:
        code, kind, origin = parse_cargo_cover_mark_row(
            mark_code,
            cover_kind,
            source_ref,
        )
        row = CargoCoverMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cover_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
