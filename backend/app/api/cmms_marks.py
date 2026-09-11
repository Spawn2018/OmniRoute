from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cmms_mark import CmmsMark
from app.services.cmms_marks.cmms_mark_service import CmmsMarkService

router = APIRouter(prefix="/cmms-marks", tags=["cmms-marks"])

_PERM = "can_manage_cmms_marks"


class CmmsMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    work_kind: str
    source_ref: str


class CmmsMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    work_kind: str
    source_ref: str


def _row(saved: CmmsMark) -> CmmsMarkResponse:
    return CmmsMarkResponse.model_validate(saved)


@router.get("", response_model=list[CmmsMarkResponse])
async def list_cmms_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CmmsMarkResponse]:
    packed = await CmmsMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CmmsMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cmms_mark(
    body: CmmsMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CmmsMarkResponse:
    saved = await CmmsMarkService(session).persist_cmms_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        work_kind=body.work_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
