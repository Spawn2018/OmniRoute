from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.party_document import PartyDocument


class PartyDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_documents(self) -> list[PartyDocument]:
        packed = await self._session.scalars(
            select(PartyDocument).order_by(
                PartyDocument.created_at.desc(),
                PartyDocument.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: PartyDocument) -> PartyDocument:
        self._session.add(row)
        await self._session.flush()
        return row
