from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inbound_message import InboundMessage


class InboundMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[InboundMessage]:
        result = await self._session.scalars(
            select(InboundMessage).order_by(InboundMessage.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: InboundMessage) -> InboundMessage:
        self._session.add(row)
        await self._session.flush()
        return row
