"""HTTP katalog metryki jobu — HITL, bez scoringu osoby i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.job_metric_mark import JobMetricMark
from app.services.job_metric_marks.job_metric_mark_service import JobMetricMarkService

router = APIRouter(prefix="/job-metric-marks", tags=["job-metric-mark"])
_PERM = "can_manage_job_metric_marks"


class JobMetricMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    metric_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class JobMetricMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    metric_kind: str
    source_ref: str


def _to_dto(row: JobMetricMark) -> JobMetricMarkResponse:
    return JobMetricMarkResponse.model_validate(row)


@router.get("", response_model=list[JobMetricMarkResponse])
async def list_job_metric_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[JobMetricMarkResponse]:
    catalog = JobMetricMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=JobMetricMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_job_metric_mark(
    body: JobMetricMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> JobMetricMarkResponse:
    catalog = JobMetricMarkService(session)
    saved = await catalog.persist_job_metric_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        metric_kind=body.metric_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "job-metric-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
