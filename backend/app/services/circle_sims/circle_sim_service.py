from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.circle_sim import (
    require_circle_pair,
    require_circle_source_ref,
    require_sim_code,
)
from app.models.circle_sim import CircleSim
from app.repositories.circle_sims.circle_sim_repository import CircleSimRepository


class CircleSimService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CircleSimRepository(session)

    async def list_rows(self) -> list[CircleSim]:
        return await self._rows.fetch_rows()

    async def persist_circle_sim(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        sim_code: object,
        unload_unlocode: object,
        load_unlocode: object,
        source_ref: object,
    ) -> CircleSim:
        unload, load = require_circle_pair(unload_unlocode, load_unlocode)
        row = CircleSim(
            id=uuid4(),
            organization_id=organization_id,
            sim_code=require_sim_code(sim_code),
            unload_unlocode=unload,
            load_unlocode=load,
            source_ref=require_circle_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._rows.add(row)
