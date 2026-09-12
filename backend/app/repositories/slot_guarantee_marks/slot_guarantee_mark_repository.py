from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.slot_guarantee_mark import SlotGuaranteeMark


def _slot_guarantee_catalog_query() -> Select[tuple[SlotGuaranteeMark]]:
    return select(SlotGuaranteeMark).order_by(
        SlotGuaranteeMark.mark_code.asc(),
        SlotGuaranteeMark.created_at.desc(),
    )


class SlotGuaranteeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SlotGuaranteeMark]:
        loaded = await self._session.scalars(_slot_guarantee_catalog_query())
        batch: Sequence[SlotGuaranteeMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: SlotGuaranteeMark) -> SlotGuaranteeMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
