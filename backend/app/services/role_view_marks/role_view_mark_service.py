from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.role_view_mark import parse_role_view_mark_row
from app.models.role_view_mark import RoleViewMark
from app.repositories.role_view_marks.role_view_mark_repository import (
    RoleViewMarkRepository,
)


class RoleViewMarkService:
    """HITL katalog widoku roli — bez board T6 i bez mapy."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = RoleViewMarkRepository(session)

    async def list_marks(self) -> list[RoleViewMark]:
        return await self._marks.list_marks()

    async def persist_role_view_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        view_kind: object,
        source_ref: object,
    ) -> RoleViewMark:
        code, kind, pointer = parse_role_view_mark_row(
            mark_code,
            view_kind,
            source_ref,
        )
        row = RoleViewMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            view_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
