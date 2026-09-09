from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prediction_ledger import PredictionLedger


class PredictionLedgerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[PredictionLedger]:
        packed = await self._session.scalars(
            select(PredictionLedger).order_by(
                PredictionLedger.created_at.desc(),
                PredictionLedger.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: PredictionLedger) -> PredictionLedger:
        self._session.add(row)
        await self._session.flush()
        return row
