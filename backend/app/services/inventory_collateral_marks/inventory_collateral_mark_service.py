from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.inventory_collateral_mark import parse_inventory_collateral_mark_row
from app.models.inventory_collateral_mark import InventoryCollateralMark
from app.repositories.inventory_collateral_marks.inventory_collateral_mark_repository import (
    InventoryCollateralMarkRepository,
)


class InventoryCollateralMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InventoryCollateralMarkRepository(session)

    async def list_marks(self) -> list[InventoryCollateralMark]:
        return await self._rows.list_marks()

    async def persist_inventory_collateral_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        collateral_kind: object,
        source_ref: object,
    ) -> InventoryCollateralMark:
        code, kind, origin = parse_inventory_collateral_mark_row(
            mark_code,
            collateral_kind,
            source_ref,
        )
        row = InventoryCollateralMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            collateral_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
