from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.article50_mark import parse_article50_mark_row
from app.models.article50_mark import Article50Mark
from app.repositories.article50_marks.article50_mark_repository import (
    Article50MarkRepository,
)


class Article50MarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = Article50MarkRepository(session)

    async def list_marks(self) -> list[Article50Mark]:
        return await self._rows.list_marks()

    async def persist_article50_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        label_kind: object,
        source_ref: object,
    ) -> Article50Mark:
        code, kind, origin = parse_article50_mark_row(
            mark_code,
            label_kind,
            source_ref,
        )
        row = Article50Mark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            label_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
