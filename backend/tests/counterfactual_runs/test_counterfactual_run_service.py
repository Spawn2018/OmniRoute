from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.domain.errors import InvalidCounterfactualRun
from app.services.counterfactual_runs.counterfactual_run_service import (
    CounterfactualRunService,
)


async def _persist(desk: CounterfactualRunService) -> None:
    await desk.persist_run(
        organization_id=uuid4(),
        user_id=uuid4(),
        run_code="fuel_spike",
        plan_snapshot_id=str(uuid4()),
        baseline_label="plan z wczoraj",
        levers_label="paliwo w gore",
        result_label="eta plus dwie godziny",
        source_ref="tenant:manual",
    )


@pytest.mark.asyncio
async def test_persist_maps_snapshot_fk_integrity() -> None:
    desk = CounterfactualRunService(AsyncMock())
    orig = Exception(
        'violates foreign key constraint "fk_counterfactual_run_snapshot"'
    )
    desk._rows.add = AsyncMock(side_effect=IntegrityError("INSERT", {}, orig))
    with pytest.raises(InvalidCounterfactualRun, match="migawka"):
        await _persist(desk)


@pytest.mark.asyncio
async def test_persist_reraises_other_integrity() -> None:
    desk = CounterfactualRunService(AsyncMock())
    orig = Exception(
        'duplicate key value violates unique constraint "uq_counterfactual_run_org_code"'
    )
    desk._rows.add = AsyncMock(side_effect=IntegrityError("INSERT", {}, orig))
    with pytest.raises(IntegrityError):
        await _persist(desk)
