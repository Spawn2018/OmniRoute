from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipment_document import (
    require_document_kind,
    require_document_shipment_id,
    require_document_source_ref,
)
from app.models.shipment_document import ShipmentDocument
from app.repositories.shipment_documents.shipment_document_repository import (
    ShipmentDocumentRepository,
)


class ShipmentDocumentService:
    def __init__(self, session: AsyncSession) -> None:
        self._documents = ShipmentDocumentRepository(session)

    async def list_documents(self) -> list[ShipmentDocument]:
        return await self._documents.list_all()

    async def record_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        document_kind: str,
        source_ref: str,
    ) -> ShipmentDocument:
        row = ShipmentDocument(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=require_document_shipment_id(shipment_id),
            document_kind=require_document_kind(document_kind),
            source_ref=require_document_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._documents.add(row)
