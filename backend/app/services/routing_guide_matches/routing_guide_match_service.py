from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.routing_guide_match import parse_routing_guide_match_row
from app.models.routing_guide_match import RoutingGuideMatch
from app.repositories.routing_guide_matches.routing_guide_match_repository import (
    RoutingGuideMatchRepository,
)


class RoutingGuideMatchService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RoutingGuideMatchRepository(session)

    async def list_marks(self) -> list[RoutingGuideMatch]:
        return await self._rows.list_marks()

    async def persist_routing_guide_match(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        match_kind: object,
        source_ref: object,
    ) -> RoutingGuideMatch:
        code, kind, origin = parse_routing_guide_match_row(
            mark_code, match_kind, source_ref
        )
        row = RoutingGuideMatch(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            match_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
