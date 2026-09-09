from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.tower_impact import (
    require_chain_stage,
    require_contract_data_status,
    require_impact_source_ref,
)
from app.models.tower_impact import TowerImpact
from app.repositories.tower_impacts.tower_impact_repository import (
    TowerImpactRepository,
)


class TowerImpactService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = TowerImpactRepository(session)

    async def list_marks(self) -> list[TowerImpact]:
        return await self._marks.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        chain_stage: object,
        contract_data_status: object,
        source_ref: object,
    ) -> TowerImpact:
        row = TowerImpact(
            id=uuid4(),
            organization_id=organization_id,
            chain_stage=require_chain_stage(chain_stage),
            contract_data_status=require_contract_data_status(contract_data_status),
            source_ref=require_impact_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.add(row)
