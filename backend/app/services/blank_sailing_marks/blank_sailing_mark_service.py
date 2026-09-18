from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.blank_sailing_mark import parse_blank_sailing_mark_row
from app.models.blank_sailing_mark import BlankSailingMark
from app.repositories.blank_sailing_marks import BlankSailingMarkRepository


class BlankSailingMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = BlankSailingMarkRepository(session)

    async def list_marks(self) -> list[BlankSailingMark]:
        return await self._rows.list_marks()

    async def persist_blank_sailing_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        sailing_kind: object,
        source_ref: object,
    ) -> BlankSailingMark:
        code, kind, origin = parse_blank_sailing_mark_row(
            mark_code,
            sailing_kind,
            source_ref,
        )
        row = BlankSailingMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            sailing_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
