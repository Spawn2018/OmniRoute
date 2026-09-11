from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.combined_transport_mark import CombinedTransportMark


class CombinedTransportMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[CombinedTransportMark]:
        packed = await self._session.scalars(
            select(CombinedTransportMark).order_by(
                CombinedTransportMark.mark_code,
                CombinedTransportMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: CombinedTransportMark) -> CombinedTransportMark:
        self._session.add(row)
        await self._session.flush()
        return row
