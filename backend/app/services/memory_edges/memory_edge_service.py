from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.memory_edge import require_edge_kind, require_edge_source_ref
from app.models.memory_edge import MemoryEdge
from app.repositories.memory_edges.memory_edge_repository import MemoryEdgeRepository


class MemoryEdgeService:
    def __init__(self, session: AsyncSession) -> None:
        self._links = MemoryEdgeRepository(session)

    async def list_links(self) -> list[MemoryEdge]:
        return await self._links.fetch_links()

    async def record_link(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        edge_kind: object,
        source_ref: object,
    ) -> MemoryEdge:
        kind = require_edge_kind(edge_kind)
        origin = require_edge_source_ref(source_ref)
        packed = MemoryEdge(
            id=uuid4(),
            organization_id=organization_id,
            edge_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._links.add(packed)
