from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.circle_sim import CircleSim


class CircleSimRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[CircleSim]:
        packed = await self._session.scalars(
            select(CircleSim).order_by(
                CircleSim.sim_code,
                CircleSim.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: CircleSim) -> CircleSim:
        self._session.add(row)
        await self._session.flush()
        return row
