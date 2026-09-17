from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.relation_document_requirement import parse_relation_document_requirement_row
from app.models.relation_document_requirement import RelationDocumentRequirement
from app.repositories.relation_document_requirements import (
    RelationDocumentRequirementRepository,
)


class RelationDocumentRequirementService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RelationDocumentRequirementRepository(session)

    async def list_marks(self) -> list[RelationDocumentRequirement]:
        return await self._rows.list_marks()

    async def persist_relation_document_requirement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        requirement_code: object,
        relation_kind: object,
        source_ref: object,
    ) -> RelationDocumentRequirement:
        code, kind, origin = parse_relation_document_requirement_row(
            requirement_code,
            relation_kind,
            source_ref,
        )
        row = RelationDocumentRequirement(
            id=uuid4(),
            organization_id=organization_id,
            requirement_code=code,
            relation_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
