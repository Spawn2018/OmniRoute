from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.working_capital_mark import parse_working_capital_mark_row
from app.models.working_capital_mark import WorkingCapitalMark
from app.repositories.working_capital_marks.working_capital_mark_repository import (
    WorkingCapitalMarkRepository,
)


class WorkingCapitalMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = WorkingCapitalMarkRepository(session)

    async def list_marks(self) -> list[WorkingCapitalMark]:
        return await self._rows.list_marks()

    async def persist_working_capital_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        capital_kind: object,
        source_ref: object,
    ) -> WorkingCapitalMark:
        code, kind, origin = parse_working_capital_mark_row(
            mark_code,
            capital_kind,
            source_ref,
        )
        row = WorkingCapitalMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            capital_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
