from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.copy_ban_mark import parse_copy_ban_mark_row
from app.models.copy_ban_mark import CopyBanMark
from app.repositories.copy_ban_marks.copy_ban_mark_repository import (
    CopyBanMarkRepository,
)


class CopyBanMarkService:
    """HITL katalog zakazu copy claimów — bez silnika banów i bez kwoty."""

    def __init__(self, session: AsyncSession) -> None:
        self._marks = CopyBanMarkRepository(session)

    async def list_marks(self) -> list[CopyBanMark]:
        return await self._marks.list_marks()

    async def persist_copy_ban_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ban_kind: object,
        source_ref: object,
    ) -> CopyBanMark:
        code, kind, pointer = parse_copy_ban_mark_row(
            mark_code,
            ban_kind,
            source_ref,
        )
        row = CopyBanMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ban_kind=kind,
            source_ref=pointer,
            created_by=user_id,
        )
        return await self._marks.add_mark(row)
