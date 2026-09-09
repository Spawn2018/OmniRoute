from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.rank_mark import require_rank_kind, require_rank_source_ref
from app.models.rank_mark import RankMark
from app.repositories.rank_marks.rank_mark_repository import RankMarkRepository


class RankMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._axes = RankMarkRepository(session)

    async def list_axes(self) -> list[RankMark]:
        return await self._axes.fetch_axes()

    async def record_axis(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        rank_kind: object,
        source_ref: object,
    ) -> RankMark:
        kind = require_rank_kind(rank_kind)
        origin = require_rank_source_ref(source_ref)
        packed = RankMark(
            id=uuid4(),
            organization_id=organization_id,
            rank_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._axes.add(packed)
