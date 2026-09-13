from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.lcl_console_mark import parse_lcl_console_mark_row
from app.models.lcl_console_mark import LclConsoleMark
from app.repositories.lcl_console_marks.lcl_console_mark_repository import (
    LclConsoleMarkRepository,
)


class LclConsoleMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LclConsoleMarkRepository(session)

    async def list_marks(self) -> list[LclConsoleMark]:
        return await self._rows.list_marks()

    async def persist_lcl_console_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        console_kind: object,
        source_ref: object,
    ) -> LclConsoleMark:
        code, kind, origin = parse_lcl_console_mark_row(
            mark_code,
            console_kind,
            source_ref,
        )
        row = LclConsoleMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            console_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
