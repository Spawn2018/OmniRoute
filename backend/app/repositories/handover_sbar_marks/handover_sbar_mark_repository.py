from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.handover_sbar_mark import HandoverSbarMark


class HandoverSbarMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[HandoverSbarMark]:
        stmt = select(HandoverSbarMark).order_by(
            HandoverSbarMark.mark_code,
            HandoverSbarMark.id,
        )
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: HandoverSbarMark) -> HandoverSbarMark:
        self._session.add(row)
        await self._session.flush()
        return row
