from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.inventory_position_mark import parse_inventory_position_mark_row
from app.models.inventory_position_mark import InventoryPositionMark
from app.repositories.inventory_position_marks.inventory_position_mark_repository import (
    InventoryPositionMarkRepository,
)


class InventoryPositionMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InventoryPositionMarkRepository(session)

    async def list_marks(self) -> list[InventoryPositionMark]:
        return await self._rows.list_marks()

    async def persist_inventory_position_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        stock_kind: object,
        source_ref: object,
    ) -> InventoryPositionMark:
        code, kind, origin = parse_inventory_position_mark_row(
            mark_code,
            stock_kind,
            source_ref,
        )
        row = InventoryPositionMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            stock_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
