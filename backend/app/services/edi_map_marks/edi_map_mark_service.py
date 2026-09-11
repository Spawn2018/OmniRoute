from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.edi_map_mark import parse_edi_map_mark_row
from app.models.edi_map_mark import EdiMapMark
from app.repositories.edi_map_marks.edi_map_mark_repository import EdiMapMarkRepository


class EdiMapMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = EdiMapMarkRepository(session)

    async def list_marks(self) -> list[EdiMapMark]:
        return await self._rows.list_marks()

    async def persist_edi_map_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        map_kind: object,
        source_ref: object,
    ) -> EdiMapMark:
        code, kind, origin = parse_edi_map_mark_row(
            mark_code,
            map_kind,
            source_ref,
        )
        row = EdiMapMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            map_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
