from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.intervention_outcome import InterventionOutcome


class InterventionOutcomeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_outcomes(self) -> list[InterventionOutcome]:
        packed = await self._session.scalars(
            select(InterventionOutcome).order_by(
                InterventionOutcome.outcome_code,
                InterventionOutcome.id,
            ),
        )
        return list(packed.all())

    async def add_outcome(self, row: InterventionOutcome) -> InterventionOutcome:
        self._session.add(row)
        await self._session.flush()
        return row
