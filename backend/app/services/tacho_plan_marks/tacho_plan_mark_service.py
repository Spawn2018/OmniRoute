from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tacho_plan_mark import parse_tacho_plan_mark_row
from app.models.tacho_plan_mark import TachoPlanMark
from app.repositories.tacho_plan_marks.tacho_plan_mark_repository import (
    TachoPlanMarkRepository,
)


class TachoPlanMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TachoPlanMarkRepository(session)

    async def list_marks(self) -> list[TachoPlanMark]:
        return await self._rows.list_marks()

    async def persist_tacho_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        constraint_kind: object,
        source_ref: object,
    ) -> TachoPlanMark:
        code, kind, origin = parse_tacho_plan_mark_row(
            mark_code,
            constraint_kind,
            source_ref,
        )
        row = TachoPlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            constraint_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
