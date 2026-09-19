from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidResource
from app.domain.resource_document import parse_resource_document
from app.models.resource_document import ResourceDocument
from app.repositories.resource_documents import ResourceDocumentRepository


class ResourceDocumentService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ResourceDocumentRepository(session)

    async def list_documents(self) -> list[ResourceDocument]:
        return await self._rows.list_documents()

    async def record_document(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        resource_id: object,
        document_kind: object,
        valid_until: object,
        source_ref: object,
    ) -> ResourceDocument:
        fleet_id, kind, until, origin = parse_resource_document(
            resource_id,
            document_kind,
            valid_until,
            source_ref,
        )
        row = ResourceDocument(
            id=uuid4(),
            organization_id=organization_id,
            resource_id=fleet_id,
            document_kind=kind,
            valid_until=until,
            source_ref=origin,
            created_by=user_id,
        )
        try:
            return await self._rows.add(row)
        except IntegrityError as exc:
            detail = str(getattr(exc, "orig", exc))
            if "fk_resource_document_resource" in detail:
                raise InvalidResource("zasób") from exc
            raise
