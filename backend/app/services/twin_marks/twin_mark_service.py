from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.twin_mark import require_twin_kind, require_twin_source_ref
from app.models.twin_mark import TwinMark
from app.repositories.twin_marks.twin_mark_repository import TwinMarkRepository


class TwinMarkService:
    def __init__(self, session: AsyncSession) -> None:
        self._store = TwinMarkRepository(session)

    async def list_marks(self) -> list[TwinMark]:
        return await self._store.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        twin_kind: object,
        source_ref: object,
    ) -> TwinMark:
        kind = require_twin_kind(twin_kind)
        origin = require_twin_source_ref(source_ref)
        packed = TwinMark(
            id=uuid4(),
            organization_id=organization_id,
            twin_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._store.add(packed)
