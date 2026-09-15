from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_pipeline_mark import CrmPipelineMark
from app.services.crm_pipeline_marks.crm_pipeline_mark_service import CrmPipelineMarkService

router = APIRouter(prefix="/crm-pipeline-marks", tags=["crm-pipeline-marks"])

_PERM = "can_manage_crm_pipeline_marks"


class CrmPipelineMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    pipeline_kind: str
    source_ref: str


class CrmPipelineMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    pipeline_kind: str
    source_ref: str


def _row(saved: CrmPipelineMark) -> CrmPipelineMarkResponse:
    return CrmPipelineMarkResponse.model_validate(saved)


@router.get("", response_model=list[CrmPipelineMarkResponse])
async def list_crm_pipeline_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmPipelineMarkResponse]:
    packed = await CrmPipelineMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CrmPipelineMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_pipeline_mark(
    body: CrmPipelineMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmPipelineMarkResponse:
    saved = await CrmPipelineMarkService(session).persist_crm_pipeline_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        pipeline_kind=body.pipeline_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
