from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.terminal_slot_connector import TerminalSlotConnector


class TerminalSlotConnectorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_rows(self) -> list[TerminalSlotConnector]:
        packed = await self._session.scalars(
            select(TerminalSlotConnector).order_by(
                TerminalSlotConnector.terminal_code,
                TerminalSlotConnector.connector_code,
                TerminalSlotConnector.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: TerminalSlotConnector) -> TerminalSlotConnector:
        self._session.add(row)
        await self._session.flush()
        return row
