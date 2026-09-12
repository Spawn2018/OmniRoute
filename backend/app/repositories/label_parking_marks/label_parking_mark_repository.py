from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.label_parking_mark import LabelParkingMark


def _label_parking_catalog_query() -> Select[tuple[LabelParkingMark]]:
    return select(LabelParkingMark).order_by(
        LabelParkingMark.mark_code.asc(),
        LabelParkingMark.created_at.desc(),
    )


class LabelParkingMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[LabelParkingMark]:
        loaded = await self._session.scalars(_label_parking_catalog_query())
        batch: Sequence[LabelParkingMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: LabelParkingMark) -> LabelParkingMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
