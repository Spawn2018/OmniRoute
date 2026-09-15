from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_dedup_mark import CrmDedupMark
from app.services.crm_dedup_marks.crm_dedup_mark_service import CrmDedupMarkService

router = APIRouter(prefix="/crm-dedup-marks", tags=["crm-dedup-marks"])

_PERM = "can_manage_crm_dedup_marks"


class CrmDedupMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    dedup_kind: str
    source_ref: str


class CrmDedupMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    dedup_kind: str
    source_ref: str


def _row(saved: CrmDedupMark) -> CrmDedupMarkResponse:
    return CrmDedupMarkResponse.model_validate(saved)


@router.get("", response_model=list[CrmDedupMarkResponse])
async def list_crm_dedup_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmDedupMarkResponse]:
    packed = await CrmDedupMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CrmDedupMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_dedup_mark(
    body: CrmDedupMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmDedupMarkResponse:
    saved = await CrmDedupMarkService(session).persist_crm_dedup_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        dedup_kind=body.dedup_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
