from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.collaboration_mark import parse_collaboration_mark_row
from app.models.collaboration_mark import CollaborationMark
from app.repositories.collaboration_marks.collaboration_mark_repository import (
    CollaborationMarkRepository,
)


class CollaborationMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CollaborationMarkRepository(session)

    async def list_marks(self) -> list[CollaborationMark]:
        return await self._rows.list_marks()

    async def persist_collaboration_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        role_kind: object,
        source_ref: object,
    ) -> CollaborationMark:
        code, kind, origin = parse_collaboration_mark_row(
            mark_code, role_kind, source_ref
        )
        row = CollaborationMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            role_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
