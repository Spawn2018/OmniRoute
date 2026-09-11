from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.routing_guide import parse_routing_guide_row
from app.models.routing_guide import RoutingGuide
from app.repositories.routing_guides.routing_guide_repository import RoutingGuideRepository


class RoutingGuideService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = RoutingGuideRepository(session)

    async def list_guides(self) -> list[RoutingGuide]:
        return await self._rows.list_guides()

    async def persist_routing_guide(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        guide_code: object,
        lane_label: object,
        mode_label: object,
        source_ref: object,
    ) -> RoutingGuide:
        code, lane, mode, origin = parse_routing_guide_row(
            guide_code, lane_label, mode_label, source_ref
        )
        row = RoutingGuide(
            id=uuid4(),
            organization_id=organization_id,
            guide_code=code,
            lane_label=lane,
            mode_label=mode,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_guide(row)
