from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.sid_import_mark import parse_sid_import_mark_row
from app.models.sid_import_mark import SidImportMark
from app.repositories.sid_import_marks.sid_import_mark_repository import (
    SidImportMarkRepository,
)


class SidImportMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = SidImportMarkRepository(session)

    async def list_marks(self) -> list[SidImportMark]:
        return await self._rows.list_marks()

    async def persist_sid_import_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sid_kind: object,
        source_ref: object,
    ) -> SidImportMark:
        code, kind, origin = parse_sid_import_mark_row(
            mark_code,
            sid_kind,
            source_ref,
        )
        row = SidImportMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sid_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
