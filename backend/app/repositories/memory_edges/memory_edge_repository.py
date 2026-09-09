from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.memory_edge import MemoryEdge


class MemoryEdgeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._db = session

    async def fetch_links(self) -> list[MemoryEdge]:
        stmt = select(MemoryEdge).order_by(MemoryEdge.edge_kind, MemoryEdge.id)
        executed = await self._db.execute(stmt)
        return list(executed.scalars())

    async def add(self, row: MemoryEdge) -> MemoryEdge:
        self._db.add(row)
        await self._db.flush()
        return row
