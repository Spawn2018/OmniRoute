from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipper_bind_mark import ShipperBindMark


class ShipperBindMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[ShipperBindMark]:
        rows = await self._session.scalars(
            select(ShipperBindMark).order_by(
                ShipperBindMark.mark_code,
                ShipperBindMark.bind_kind,
                ShipperBindMark.id,
            ),
        )
        return list(rows.all())

    async def add_mark(self, row: ShipperBindMark) -> ShipperBindMark:
        self._session.add(row)
        await self._session.flush()
        await self._session.refresh(row)
        return row
