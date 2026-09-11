from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.subcontract_edge_mark import SubcontractEdgeMark


class SubcontractEdgeMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[SubcontractEdgeMark]:
        packed = await self._session.scalars(
            select(SubcontractEdgeMark).order_by(
                SubcontractEdgeMark.mark_code,
                SubcontractEdgeMark.id,
            ),
        )
        return list(packed.all())

    async def add_mark(self, row: SubcontractEdgeMark) -> SubcontractEdgeMark:
        self._session.add(row)
        await self._session.flush()
        return row
