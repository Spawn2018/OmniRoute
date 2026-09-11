from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.impact_scenario import ImpactScenario


class ImpactScenarioRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_scenarios(self) -> list[ImpactScenario]:
        packed = await self._session.scalars(
            select(ImpactScenario).order_by(
                ImpactScenario.scenario_code,
                ImpactScenario.id,
            ),
        )
        return list(packed.all())

    async def add_scenario(self, row: ImpactScenario) -> ImpactScenario:
        self._session.add(row)
        await self._session.flush()
        return row
