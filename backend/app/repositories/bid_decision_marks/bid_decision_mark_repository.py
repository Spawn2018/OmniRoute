from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bid_decision_mark import BidDecisionMark


def _bid_decision_catalog_query() -> Select[tuple[BidDecisionMark]]:
    return select(BidDecisionMark).order_by(
        BidDecisionMark.mark_code.asc(),
        BidDecisionMark.created_at.desc(),
    )


class BidDecisionMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[BidDecisionMark]:
        loaded = await self._session.scalars(_bid_decision_catalog_query())
        batch: Sequence[BidDecisionMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: BidDecisionMark) -> BidDecisionMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
