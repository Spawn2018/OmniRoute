from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.fuel_card_mark import FuelCardMark


def _fuel_card_catalog_query() -> Select[tuple[FuelCardMark]]:
    return select(FuelCardMark).order_by(
        FuelCardMark.mark_code.asc(),
        FuelCardMark.created_at.desc(),
    )


class FuelCardMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[FuelCardMark]:
        loaded = await self._session.scalars(_fuel_card_catalog_query())
        batch: Sequence[FuelCardMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: FuelCardMark) -> FuelCardMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
