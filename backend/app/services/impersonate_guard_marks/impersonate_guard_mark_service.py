from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.impersonate_guard_mark import parse_impersonate_guard_mark_row
from app.models.impersonate_guard_mark import ImpersonateGuardMark
from app.repositories.impersonate_guard_marks.impersonate_guard_mark_repository import (
    ImpersonateGuardMarkRepository,
)


class ImpersonateGuardMarkService:
    """HITL katalog impersonate≠unwrap — bez crypto i bez Auth0 live."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = ImpersonateGuardMarkRepository(session)

    async def list_marks(self) -> list[ImpersonateGuardMark]:
        return await self._marks.list_marks()

    async def persist_impersonate_guard_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        guard_kind: object,
        source_ref: object,
    ) -> ImpersonateGuardMark:
        code, kind, pointer = parse_impersonate_guard_mark_row(
            mark_code,
            guard_kind,
            source_ref,
        )
        row = ImpersonateGuardMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            guard_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
