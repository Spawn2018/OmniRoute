from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.edi_message import EdiMessage


class EdiMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[EdiMessage]:
        result = await self._session.scalars(
            select(EdiMessage).order_by(EdiMessage.created_at.desc()),
        )
        return list(result.all())

    async def add(self, row: EdiMessage) -> EdiMessage:
        self._session.add(row)
        await self._session.flush()
        return row
