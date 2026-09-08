from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pallet_balance import PalletBalance


class PalletBalanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[PalletBalance]:
        result = await self._session.scalars(
            select(PalletBalance).order_by(
                PalletBalance.created_at.desc(),
                PalletBalance.id,
            ),
        )
        return list(result.all())

    async def add(self, row: PalletBalance) -> PalletBalance:
        self._session.add(row)
        await self._session.flush()
        return row
