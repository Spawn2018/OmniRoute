from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dual_ledger_mark import DualLedgerMark


def _dual_ledger_catalog_query() -> Select[tuple[DualLedgerMark]]:
    return select(DualLedgerMark).order_by(
        DualLedgerMark.mark_code.asc(),
        DualLedgerMark.created_at.desc(),
    )


class DualLedgerMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DualLedgerMark]:
        loaded = await self._session.scalars(_dual_ledger_catalog_query())
        batch: Sequence[DualLedgerMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: DualLedgerMark) -> DualLedgerMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
