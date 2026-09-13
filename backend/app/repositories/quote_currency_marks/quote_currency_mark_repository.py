from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quote_currency_mark import QuoteCurrencyMark


def _bid_decision_catalog_query() -> Select[tuple[QuoteCurrencyMark]]:
    return select(QuoteCurrencyMark).order_by(
        QuoteCurrencyMark.mark_code.asc(),
        QuoteCurrencyMark.created_at.desc(),
    )

class QuoteCurrencyMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[QuoteCurrencyMark]:
        loaded = await self._session.scalars(_bid_decision_catalog_query())
        batch: Sequence[QuoteCurrencyMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: QuoteCurrencyMark) -> QuoteCurrencyMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
