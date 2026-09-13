from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.twin_kind import TwinKind


def _kind_query() -> Select[tuple[TwinKind]]:
    return select(TwinKind).order_by(TwinKind.created_at.desc(), TwinKind.id)


class TwinKindRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[TwinKind]:
        loaded = await self._session.scalars(_kind_query())
        batch: Sequence[TwinKind] = loaded.all()
        return list(batch)

    async def add(self, entity: TwinKind) -> TwinKind:
        self._session.add(entity)
        await self._session.flush()
        return entity
