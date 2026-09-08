from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_template import DocumentTemplate


class DocumentTemplateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[DocumentTemplate]:
        result = await self._session.scalars(
            select(DocumentTemplate).order_by(
                DocumentTemplate.created_at.desc(),
                DocumentTemplate.id,
            ),
        )
        return list(result.all())

    async def add(self, row: DocumentTemplate) -> DocumentTemplate:
        self._session.add(row)
        await self._session.flush()
        return row
