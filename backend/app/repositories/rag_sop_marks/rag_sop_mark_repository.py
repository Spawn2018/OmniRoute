from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rag_sop_mark import RagSopMark


def _rag_sop_catalog_query() -> Select[tuple[RagSopMark]]:
    return select(RagSopMark).order_by(
        RagSopMark.mark_code.asc(),
        RagSopMark.created_at.desc(),
    )


class RagSopMarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_marks(self) -> list[RagSopMark]:
        loaded = await self._session.scalars(_rag_sop_catalog_query())
        batch: Sequence[RagSopMark] = loaded.all()
        return list(batch)

    async def add_mark(self, entity: RagSopMark) -> RagSopMark:
        self._session.add(entity)
        await self._session.flush()
        return entity
