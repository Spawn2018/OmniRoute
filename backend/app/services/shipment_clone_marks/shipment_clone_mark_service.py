from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.shipment_clone_mark import parse_shipment_clone_mark_row
from app.models.shipment_clone_mark import ShipmentCloneMark
from app.repositories.shipment_clone_marks.shipment_clone_mark_repository import (
    ShipmentCloneMarkRepository,
)


class ShipmentCloneMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ShipmentCloneMarkRepository(session)

    async def list_marks(self) -> list[ShipmentCloneMark]:
        return await self._rows.list_marks()

    async def persist_shipment_clone_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        clone_kind: object,
        source_ref: object,
    ) -> ShipmentCloneMark:
        code, kind, origin = parse_shipment_clone_mark_row(
            mark_code,
            clone_kind,
            source_ref,
        )
        row = ShipmentCloneMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            clone_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
