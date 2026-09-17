from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.relation_document_requirement import RelationDocumentRequirement


class RelationDocumentRequirementRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RelationDocumentRequirement]:
        packed = await self._session.scalars(
            select(RelationDocumentRequirement).order_by(
                RelationDocumentRequirement.requirement_code,
                RelationDocumentRequirement.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: RelationDocumentRequirement) -> RelationDocumentRequirement:
        self._session.add(row)
        await self._session.flush()
        return row
