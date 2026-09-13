from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.benefit_ledger import BenefitLedger


def _ledger_query() -> Select[tuple[BenefitLedger]]:
    return select(BenefitLedger).order_by(
        BenefitLedger.created_at.desc(),
        BenefitLedger.id,
    )


class BenefitLedgerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[BenefitLedger]:
        loaded = await self._session.scalars(_ledger_query())
        batch: Sequence[BenefitLedger] = loaded.all()
        return list(batch)

    async def add(self, entity: BenefitLedger) -> BenefitLedger:
        self._session.add(entity)
        await self._session.flush()
        return entity
