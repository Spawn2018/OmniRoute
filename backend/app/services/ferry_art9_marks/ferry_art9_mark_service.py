from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ferry_art9_mark import parse_ferry_art9_mark_row
from app.models.ferry_art9_mark import FerryArt9Mark
from app.repositories.ferry_art9_marks.ferry_art9_mark_repository import (
    FerryArt9MarkRepository,
)


class FerryArt9MarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = FerryArt9MarkRepository(session)

    async def list_marks(self) -> list[FerryArt9Mark]:
        return await self._rows.list_marks()

    async def persist_ferry_art9_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        ferry_kind: object,
        source_ref: object,
    ) -> FerryArt9Mark:
        code, kind, origin = parse_ferry_art9_mark_row(
            mark_code,
            ferry_kind,
            source_ref,
        )
        row = FerryArt9Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            ferry_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
