from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pallet_ledger import PalletLedger


class PalletLedgerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[PalletLedger]:
        result = await self._session.scalars(
            select(PalletLedger).order_by(
                PalletLedger.created_at.desc(),
                PalletLedger.id,
            ),
        )
        return list(result.all())

    async def add(self, row: PalletLedger) -> PalletLedger:
        self._session.add(row)
        await self._session.flush()
        return row
