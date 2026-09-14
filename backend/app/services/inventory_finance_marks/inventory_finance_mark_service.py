from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.inventory_finance_mark import parse_inventory_finance_mark_row
from app.models.inventory_finance_mark import InventoryFinanceMark
from app.repositories.inventory_finance_marks.inventory_finance_mark_repository import (
    InventoryFinanceMarkRepository,
)


class InventoryFinanceMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InventoryFinanceMarkRepository(session)

    async def list_marks(self) -> list[InventoryFinanceMark]:
        return await self._rows.list_marks()

    async def persist_inventory_finance_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        mark_code: object,
        finance_kind: object,
        source_ref: object,
    ) -> InventoryFinanceMark:
        code, kind, origin = parse_inventory_finance_mark_row(
            mark_code,
            finance_kind,
            source_ref,
        )
        row = InventoryFinanceMark(
            id=uuid4(),
            organization_id=organization_id,
            mark_code=code,
            finance_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_mark(row)
