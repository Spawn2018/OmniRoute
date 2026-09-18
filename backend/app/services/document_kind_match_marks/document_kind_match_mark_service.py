from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.document_kind_match_mark import parse_document_kind_match_mark_row
from app.models.document_kind_match_mark import DocumentKindMatchMark
from app.repositories.document_kind_match_marks import DocumentKindMatchMarkRepository


class DocumentKindMatchMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = DocumentKindMatchMarkRepository(session)

    async def list_marks(self) -> list[DocumentKindMatchMark]:
        return await self._rows.list_marks()

    async def persist_document_kind_match_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> DocumentKindMatchMark:
        code, kind, origin = parse_document_kind_match_mark_row(
            mark_code,
            match_kind,
            source_ref,
        )
        row = DocumentKindMatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
