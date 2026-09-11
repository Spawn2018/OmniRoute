from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fuel_anomaly_mark import FuelAnomalyMark


class FuelAnomalyMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FuelAnomalyMark]:
        packed = await self._session.scalars(
            select(FuelAnomalyMark).order_by(
                FuelAnomalyMark.mark_code,
                FuelAnomalyMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: FuelAnomalyMark) -> FuelAnomalyMark:
        self._session.add(row)
        await self._session.flush()
        return row
