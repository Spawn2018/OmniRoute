from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.suggestion_ledger import SuggestionLedger


def _suggestion_ledger_query() -> Select[tuple[SuggestionLedger]]:
    return select(SuggestionLedger).order_by(
        SuggestionLedger.created_at.desc(),
        SuggestionLedger.id,
    )


class SuggestionLedgerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[SuggestionLedger]:
        loaded = await self._session.scalars(_suggestion_ledger_query())
        batch: Sequence[SuggestionLedger] = loaded.all()
        return list(batch)

    async def add(self, entity: SuggestionLedger) -> SuggestionLedger:
        self._session.add(entity)
        await self._session.flush()
        return entity
