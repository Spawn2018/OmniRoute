from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.outcome_kind import OutcomeKind


def _kind_query() -> Select[tuple[OutcomeKind]]:
    return select(OutcomeKind).order_by(
        OutcomeKind.created_at.desc(),
        OutcomeKind.id,
    )


class OutcomeKindRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[OutcomeKind]:
        loaded = await self._session.scalars(_kind_query())
        batch: Sequence[OutcomeKind] = loaded.all()
        return list(batch)

    async def add(self, entity: OutcomeKind) -> OutcomeKind:
        self._session.add(entity)
        await self._session.flush()
        return entity
