from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.e_delivery_mark import EDeliveryMark


class EDeliveryMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[EDeliveryMark]:
        packed = await self._session.scalars(
            select(EDeliveryMark).order_by(
                EDeliveryMark.mark_code,
                EDeliveryMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: EDeliveryMark) -> EDeliveryMark:
        self._session.add(row)
        await self._session.flush()
        return row
