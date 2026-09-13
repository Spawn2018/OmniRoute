"""HTTP katalog przebiegu what-if — HITL etykiety, bez silnika."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.counterfactual_run import CounterfactualRun
from app.services.counterfactual_runs.counterfactual_run_service import (
    CounterfactualRunService,
)

router = APIRouter(prefix="/counterfactual-runs", tags=["counterfactual-runs"])
_PERM = "can_manage_counterfactual_runs"


class CounterfactualRunCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    run_code: str = Field(min_length=2, max_length=32)
    baseline_label: str = Field(min_length=1, max_length=256)
    levers_label: str = Field(min_length=1, max_length=256)
    result_label: str = Field(min_length=1, max_length=256)
    source_ref: str = Field(min_length=1, max_length=256)


class CounterfactualRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    run_code: str
    baseline_label: str
    levers_label: str
    result_label: str
    source_ref: str


def _as_row(row: CounterfactualRun) -> CounterfactualRunResponse:
    return CounterfactualRunResponse(
        id=row.id,
        organization_id=row.organization_id,
        run_code=row.run_code,
        baseline_label=row.baseline_label,
        levers_label=row.levers_label,
        result_label=row.result_label,
        source_ref=row.source_ref,
    )


@router.get("", response_model=list[CounterfactualRunResponse])
async def list_counterfactual_runs(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CounterfactualRunResponse]:
    rows = await CounterfactualRunService(session).list_rows()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=CounterfactualRunResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_counterfactual_run(
    body: CounterfactualRunCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CounterfactualRunResponse:
    saved = await CounterfactualRunService(session).persist_run(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        run_code=body.run_code,
        baseline_label=body.baseline_label,
        levers_label=body.levers_label,
        result_label=body.result_label,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "counterfactual-run"
    response.headers["X-Omni-Mode"] = "hitl"
    return _as_row(saved)
