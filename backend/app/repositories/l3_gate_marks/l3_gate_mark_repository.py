from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.l3_gate_mark import L3GateMark


class L3GateMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[L3GateMark]:
        stmt = select(L3GateMark).order_by(
            L3GateMark.mark_code,
            L3GateMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: L3GateMark) -> L3GateMark:
        self._session.add(row)
        await self._session.flush()
        return row
