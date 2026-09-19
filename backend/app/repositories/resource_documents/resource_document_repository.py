from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource_document import ResourceDocument


class ResourceDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_documents(self) -> list[ResourceDocument]:
        packed = await self._session.scalars(
            select(ResourceDocument).order_by(
                ResourceDocument.valid_until,
                ResourceDocument.id,
            ),
        )
        return list(packed.all())

    async def add(self, row: ResourceDocument) -> ResourceDocument:
        self._session.add(row)
        await self._session.flush()
        return row
