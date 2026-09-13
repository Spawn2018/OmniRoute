from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.circle_sim import CircleSim
from app.models.circle_sim_pair import CircleSimPair


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

    async def list_pairs(self) -> list[CircleSimPair]:
        packed = await self._session.scalars(
            select(CircleSimPair).order_by(
                CircleSimPair.left_sim_code,
                CircleSimPair.right_sim_code,
                CircleSimPair.left_sim_id,
            ),
        )
        batch: Sequence[CircleSimPair] = packed.all()
        return list(batch)

    async def add(self, row: CircleSim) -> CircleSim:
        self._session.add(row)
        await self._session.flush()
        return row
