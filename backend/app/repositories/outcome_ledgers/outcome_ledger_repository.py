from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outcome_ledger import OutcomeLedger


def _outcome_ledger_query() -> Select[tuple[OutcomeLedger]]:
    return select(OutcomeLedger).order_by(
        OutcomeLedger.created_at.desc(),
        OutcomeLedger.id,
    )


class OutcomeLedgerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[OutcomeLedger]:
        loaded = await self._session.scalars(_outcome_ledger_query())
        batch: Sequence[OutcomeLedger] = loaded.all()
        return list(batch)

    async def add(self, entity: OutcomeLedger) -> OutcomeLedger:
        self._session.add(entity)
        await self._session.flush()
        return entity
