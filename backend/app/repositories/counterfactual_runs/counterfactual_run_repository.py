from collections.abc import Sequence

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.counterfactual_run import CounterfactualRun
from app.models.what_if_replay import WhatIfReplay


def _run_query() -> Select[tuple[CounterfactualRun]]:
    return select(CounterfactualRun).order_by(
        CounterfactualRun.created_at.desc(),
        CounterfactualRun.id,
    )


class CounterfactualRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_rows(self) -> list[CounterfactualRun]:
        loaded = await self._session.scalars(_run_query())
        batch: Sequence[CounterfactualRun] = loaded.all()
        return list(batch)

    async def list_replays(self) -> list[WhatIfReplay]:
        loaded = await self._session.scalars(
            select(WhatIfReplay).order_by(WhatIfReplay.run_code, WhatIfReplay.run_id)
        )
        batch: Sequence[WhatIfReplay] = loaded.all()
        return list(batch)

    async def add(self, entity: CounterfactualRun) -> CounterfactualRun:
        self._session.add(entity)
        await self._session.flush()
        return entity
