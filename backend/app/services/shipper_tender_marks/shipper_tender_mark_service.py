from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipper_tender_mark import parse_shipper_tender_mark_row
from app.models.shipper_tender_mark import ShipperTenderMark
from app.repositories.shipper_tender_marks.shipper_tender_mark_repository import (
    ShipperTenderMarkRepository,
)


class ShipperTenderMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipperTenderMarkRepository(session)

    async def list_marks(self) -> list[ShipperTenderMark]:
        return await self._rows.list_marks()

    async def persist_shipper_tender_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        shipper_kind: object,
        source_ref: object,
    ) -> ShipperTenderMark:
        code, kind, origin = parse_shipper_tender_mark_row(
            mark_code,
            shipper_kind,
            source_ref,
        )
        row = ShipperTenderMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            shipper_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
