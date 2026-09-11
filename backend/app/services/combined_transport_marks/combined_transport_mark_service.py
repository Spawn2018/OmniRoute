from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.combined_transport_mark import parse_combined_transport_mark_row
from app.models.combined_transport_mark import CombinedTransportMark
from app.repositories.combined_transport_marks.combined_transport_mark_repository import (
    CombinedTransportMarkRepository,
)


class CombinedTransportMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CombinedTransportMarkRepository(session)

    async def list_marks(self) -> list[CombinedTransportMark]:
        return await self._rows.list_marks()

    async def persist_combined_transport_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        regime_kind: object,
        source_ref: object,
    ) -> CombinedTransportMark:
        code, kind, origin = parse_combined_transport_mark_row(
            mark_code,
            regime_kind,
            source_ref,
        )
        row = CombinedTransportMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            regime_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
