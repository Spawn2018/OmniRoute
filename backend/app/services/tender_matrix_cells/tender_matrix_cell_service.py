from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tender_matrix_cell import (
    require_board_id,
    require_cell_amount,
    require_cell_code,
    require_cell_currency,
    require_cell_source_ref,
)
from app.models.tender_matrix_cell import TenderMatrixCell
from app.repositories.tender_matrix_cells.tender_matrix_cell_repository import (
    TenderMatrixCellRepository,
)


class TenderMatrixCellService:
    def __init__(self, session: AsyncSession) -> None:
        self._cells = TenderMatrixCellRepository(session)

    async def list_cells(self) -> list[TenderMatrixCell]:
        return await self._cells.fetch_cells()

    async def record_cell(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        tender_id: object,
        cell_code: object,
        amount: object,
        currency: object,
        source_ref: object,
    ) -> TenderMatrixCell:
        row = TenderMatrixCell(
            id=uuid4(),
            organization_id=organization_id,
            tender_id=require_board_id(tender_id),
            cell_code=require_cell_code(cell_code),
            amount=require_cell_amount(amount),
            currency=require_cell_currency(currency),
            source_ref=require_cell_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._cells.add(row)
