from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.load_plan_mark import parse_load_plan_mark_row
from app.models.load_plan_mark import LoadPlanMark
from app.repositories.load_plan_marks.load_plan_mark_repository import LoadPlanMarkRepository


class LoadPlanMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = LoadPlanMarkRepository(session)

    async def list_marks(self) -> list[LoadPlanMark]:
        return await self._rows.list_marks()

    async def persist_load_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stance_kind: object,
        source_ref: object,
    ) -> LoadPlanMark:
        code, kind, origin = parse_load_plan_mark_row(
            mark_code,
            stance_kind,
            source_ref,
        )
        row = LoadPlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
