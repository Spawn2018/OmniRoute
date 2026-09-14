from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.wms_flow_mark import WmsFlowMark


class WmsFlowMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[WmsFlowMark]:
        stmt = select(WmsFlowMark).order_by(WmsFlowMark.mark_code, WmsFlowMark.id)
        return list((await self._session.scalars(stmt)).all())

    async def add_mark(self, row: WmsFlowMark) -> WmsFlowMark:
        self._session.add(row)
        await self._session.flush()
        return row
