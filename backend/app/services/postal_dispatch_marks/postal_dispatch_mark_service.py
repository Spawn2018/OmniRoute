from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.postal_dispatch_mark import parse_postal_dispatch_mark_row
from app.models.postal_dispatch_mark import PostalDispatchMark
from app.repositories.postal_dispatch_marks.postal_dispatch_mark_repository import (
    PostalDispatchMarkRepository,
)


class PostalDispatchMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PostalDispatchMarkRepository(session)

    async def list_marks(self) -> list[PostalDispatchMark]:
        return await self._rows.list_marks()

    async def persist_postal_dispatch_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        dispatch_kind: object,
        source_ref: object,
    ) -> PostalDispatchMark:
        code, kind, origin = parse_postal_dispatch_mark_row(
            mark_code,
            dispatch_kind,
            source_ref,
        )
        row = PostalDispatchMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            dispatch_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
