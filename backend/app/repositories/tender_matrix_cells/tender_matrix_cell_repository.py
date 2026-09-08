from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tender_matrix_cell import TenderMatrixCell


class TenderMatrixCellRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def fetch_cells(self) -> list[TenderMatrixCell]:
        result = await self._session.scalars(
            select(TenderMatrixCell).order_by(
                TenderMatrixCell.created_at.desc(),
                TenderMatrixCell.id,
            ),
        )
        return list(result.all())

    async def add(self, row: TenderMatrixCell) -> TenderMatrixCell:
        self._session.add(row)
        await self._session.flush()
        return row
