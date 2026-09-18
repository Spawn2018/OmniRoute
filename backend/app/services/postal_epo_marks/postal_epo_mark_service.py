from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.postal_epo_mark import parse_postal_epo_mark_row
from app.models.postal_epo_mark import PostalEpoMark
from app.repositories.postal_epo_marks import PostalEpoMarkRepository


class PostalEpoMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = PostalEpoMarkRepository(session)

    async def list_marks(self) -> list[PostalEpoMark]:
        return await self._rows.list_marks()

    async def persist_postal_epo_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        epo_kind: object,
        source_ref: object,
    ) -> PostalEpoMark:
        code, kind, origin = parse_postal_epo_mark_row(mark_code, epo_kind, source_ref)
        row = PostalEpoMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            epo_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
