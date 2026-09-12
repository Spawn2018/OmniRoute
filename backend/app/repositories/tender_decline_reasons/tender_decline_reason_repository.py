from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_decline_reason import TenderDeclineReason


def _ordered_catalog() -> Select[tuple[TenderDeclineReason]]:
    return select(TenderDeclineReason).order_by(
        TenderDeclineReason.created_at.desc(),
        TenderDeclineReason.mark_code.asc(),
    )


class TenderDeclineReasonRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def list_marks(self) -> list[TenderDeclineReason]:
        result = await self._db.scalars(_ordered_catalog())
        rows: Sequence[TenderDeclineReason] = result.all()
        return list(rows)

    async def add_mark(self, entity: TenderDeclineReason) -> TenderDeclineReason:
        self._db.add(entity)
        await self._db.flush()
        return entity
