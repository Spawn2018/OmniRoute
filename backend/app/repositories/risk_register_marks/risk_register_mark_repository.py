from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.risk_register_mark import RiskRegisterMark


class RiskRegisterMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RiskRegisterMark]:
        stmt = select(RiskRegisterMark).order_by(
            RiskRegisterMark.mark_code,
            RiskRegisterMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: RiskRegisterMark) -> RiskRegisterMark:
        self._session.add(row)
        await self._session.flush()
        return row
