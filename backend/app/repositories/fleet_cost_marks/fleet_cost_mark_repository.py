from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fleet_cost_mark import FleetCostMark


class FleetCostMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FleetCostMark]:
        packed = await self._session.scalars(
            select(FleetCostMark).order_by(
                FleetCostMark.mark_code,
                FleetCostMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FleetCostMark) -> FleetCostMark:
        self._session.add(row)
        await self._session.flush()
        return row
