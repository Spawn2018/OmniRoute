from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.intervention_outcome import parse_intervention_outcome_row
from app.models.intervention_outcome import InterventionOutcome
from app.repositories.intervention_outcomes.intervention_outcome_repository import (
    InterventionOutcomeRepository,
)


class InterventionOutcomeService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = InterventionOutcomeRepository(session)

    async def list_outcomes(self) -> list[InterventionOutcome]:
        return await self._rows.list_outcomes()

    async def persist_intervention_outcome(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        outcome_code: object,
        result_kind: object,
        source_ref: object,
    ) -> InterventionOutcome:
        code, kind, origin = parse_intervention_outcome_row(
            outcome_code,
            result_kind,
            source_ref,
        )
        row = InterventionOutcome(
            id=uuid4(),
            organization_id=organization_id,
            outcome_code=code,
            result_kind=kind,
            source_ref=origin,
            created_by=user_id,
        )
        return await self._rows.add_outcome(row)
