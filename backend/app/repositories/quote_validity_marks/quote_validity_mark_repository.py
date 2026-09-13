from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quote_validity_mark import QuoteValidityMark


def _quote_validity_catalog_query() -> Select[tuple[QuoteValidityMark]]:
    return select(QuoteValidityMark).order_by(
        QuoteValidityMark.mark_code.asc(),
        QuoteValidityMark.created_at.desc(),
    )


class QuoteValidityMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[QuoteValidityMark]:
        loaded = await self._session.scalars(_quote_validity_catalog_query())
        batch: Sequence[QuoteValidityMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: QuoteValidityMark) -> QuoteValidityMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
