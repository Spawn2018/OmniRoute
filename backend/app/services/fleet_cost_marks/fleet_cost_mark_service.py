from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.fleet_cost_mark import parse_fleet_cost_mark_row
from app.models.fleet_cost_mark import FleetCostMark
from app.repositories.fleet_cost_marks.fleet_cost_mark_repository import (
    FleetCostMarkRepository,
)


class FleetCostMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FleetCostMarkRepository(session)

    async def list_marks(self) -> list[FleetCostMark]:
        return await self._rows.list_marks()

    async def persist_fleet_cost_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        cost_kind: object,
        source_ref: object,
    ) -> FleetCostMark:
        code, kind, origin = parse_fleet_cost_mark_row(
            mark_code,
            cost_kind,
            source_ref,
        )
        row = FleetCostMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            cost_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
