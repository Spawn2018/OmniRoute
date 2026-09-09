from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.party_document import (
    require_document_kind,
    require_party_document_source_ref,
    require_party_id,
)
from app.models.party_document import PartyDocument
from app.repositories.party_documents.party_document_repository import (
    PartyDocumentRepository,
)


class PartyDocumentService:
    def __init__(self, session: AsyncSession) -> None:
        self._documents = PartyDocumentRepository(session)

    async def list_documents(self) -> list[PartyDocument]:
        return await self._documents.fetch_documents()

    async def persist_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        party_id: object,
        document_kind: object,
        source_ref: object,
    ) -> PartyDocument:
        row = PartyDocument(
            id=uuid4(),
            organization_id=organization_id,
            party_id=require_party_id(party_id),
            document_kind=require_document_kind(document_kind),
            source_ref=require_party_document_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._documents.add(row)
