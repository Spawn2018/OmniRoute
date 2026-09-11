from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cmms_mark import parse_cmms_mark_row
from app.models.cmms_mark import CmmsMark
from app.repositories.cmms_marks.cmms_mark_repository import CmmsMarkRepository


class CmmsMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CmmsMarkRepository(session)

    async def list_marks(self) -> list[CmmsMark]:
        return await self._rows.list_marks()

    async def persist_cmms_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        work_kind: object,
        source_ref: object,
    ) -> CmmsMark:
        code, kind, origin = parse_cmms_mark_row(
            mark_code,
            work_kind,
            source_ref,
        )
        row = CmmsMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            work_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
