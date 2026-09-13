from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.route_plan_mark import parse_route_plan_mark_row
from app.models.route_plan_mark import RoutePlanMark
from app.repositories.route_plan_marks.route_plan_mark_repository import (
    RoutePlanMarkRepository,
)


class RoutePlanMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RoutePlanMarkRepository(session)

    async def list_marks(self) -> list[RoutePlanMark]:
        return await self._rows.list_marks()

    async def persist_route_plan_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        plan_kind: object,
        source_ref: object,
    ) -> RoutePlanMark:
        code, kind, origin = parse_route_plan_mark_row(
            mark_code,
            plan_kind,
            source_ref,
        )
        row = RoutePlanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            plan_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
