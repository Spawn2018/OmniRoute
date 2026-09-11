from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.routing_guide_enforcement import parse_routing_guide_enforcement_row
from app.models.routing_guide_enforcement import RoutingGuideEnforcement
from app.repositories.routing_guide_enforcements.routing_guide_enforcement_repository import (
    RoutingGuideEnforcementRepository,
)


class RoutingGuideEnforcementService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RoutingGuideEnforcementRepository(session)

    async def list_marks(self) -> list[RoutingGuideEnforcement]:
        return await self._rows.list_marks()

    async def persist_routing_guide_enforcement(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        enforcement_kind: object,
        source_ref: object,
    ) -> RoutingGuideEnforcement:
        code, kind, origin = parse_routing_guide_enforcement_row(
            mark_code, enforcement_kind, source_ref
        )
        row = RoutingGuideEnforcement(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            enforcement_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
