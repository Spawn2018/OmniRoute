from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.counterfactual_run import CounterfactualRunDraft, parse_counterfactual_run_row
from app.models.counterfactual_run import CounterfactualRun
from app.repositories.counterfactual_runs.counterfactual_run_repository import (
    CounterfactualRunRepository,
)


def _as_entity(
    organization_id: UUID,
    user_id: UUID,
    draft: CounterfactualRunDraft,
) -> CounterfactualRun:
    return CounterfactualRun(
        id=uuid4(),
        organization_id=organization_id,
        run_code=draft.run_code,
        baseline_label=draft.baseline_label,
        levers_label=draft.levers_label,
        result_label=draft.result_label,
        source_ref=draft.source_ref,
        created_by=user_id,
    )


class CounterfactualRunService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = CounterfactualRunRepository(session)

    async def list_rows(self) -> list[CounterfactualRun]:
        return await self._rows.list_rows()

    async def persist_run(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        run_code: object,
        baseline_label: object,
        levers_label: object,
        result_label: object,
        source_ref: object,
    ) -> CounterfactualRun:
        draft = parse_counterfactual_run_row(
            run_code,
            baseline_label,
            levers_label,
            result_label,
            source_ref,
        )
        return await self._rows.add(_as_entity(organization_id, user_id, draft))
