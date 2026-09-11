from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.impact_scenario import parse_impact_scenario_row
from app.models.impact_scenario import ImpactScenario
from app.repositories.impact_scenarios.impact_scenario_repository import (
    ImpactScenarioRepository,
)


class ImpactScenarioService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ImpactScenarioRepository(session)

    async def list_scenarios(self) -> list[ImpactScenario]:
        return await self._rows.list_scenarios()

    async def persist_impact_scenario(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        scenario_code: object,
        chain_label: object,
        source_ref: object,
    ) -> ImpactScenario:
        code, label, origin = parse_impact_scenario_row(
            scenario_code, chain_label, source_ref
        )
        row = ImpactScenario(
            id=uuid4(),
            organization_id=organization_id,
            scenario_code=code,
            chain_label=label,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_scenario(row)
