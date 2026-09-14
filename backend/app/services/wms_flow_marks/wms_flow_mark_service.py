from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.wms_flow_mark import parse_wms_flow_mark_row
from app.models.wms_flow_mark import WmsFlowMark
from app.repositories.wms_flow_marks.wms_flow_mark_repository import WmsFlowMarkRepository


class WmsFlowMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = WmsFlowMarkRepository(session)

    async def list_marks(self) -> list[WmsFlowMark]:
        return await self._rows.list_marks()

    async def persist_wms_flow_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        flow_kind: object,
        source_ref: object,
    ) -> WmsFlowMark:
        code, kind, origin = parse_wms_flow_mark_row(mark_code, flow_kind, source_ref)
        row = WmsFlowMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            flow_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
