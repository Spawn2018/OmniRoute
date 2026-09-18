from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_kind_match_mark import DocumentKindMatchMark


class DocumentKindMatchMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[DocumentKindMatchMark]:
        packed = await self._session.scalars(
            select(DocumentKindMatchMark).order_by(
                DocumentKindMatchMark.mark_code,
                DocumentKindMatchMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: DocumentKindMatchMark) -> DocumentKindMatchMark:
        self._session.add(row)
        await self._session.flush()
        return row
