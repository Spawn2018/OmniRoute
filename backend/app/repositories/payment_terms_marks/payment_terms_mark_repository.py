from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_terms_mark import PaymentTermsMark


def _payment_terms_catalog_query() -> Select[tuple[PaymentTermsMark]]:
    return select(PaymentTermsMark).order_by(
        PaymentTermsMark.mark_code.asc(),
        PaymentTermsMark.created_at.desc(),
    )


class PaymentTermsMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[PaymentTermsMark]:
        loaded = await self._session.scalars(_payment_terms_catalog_query())
        batch: Sequence[PaymentTermsMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: PaymentTermsMark) -> PaymentTermsMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
