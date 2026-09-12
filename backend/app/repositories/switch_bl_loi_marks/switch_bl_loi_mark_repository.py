from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.switch_bl_loi_mark import SwitchBlLoiMark


class SwitchBlLoiMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SwitchBlLoiMark]:
        packed = await self._session.scalars(
            select(SwitchBlLoiMark).order_by(
                SwitchBlLoiMark.mark_code,
                SwitchBlLoiMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SwitchBlLoiMark) -> SwitchBlLoiMark:
        self._session.add(row)
        await self._session.flush()
        return row
