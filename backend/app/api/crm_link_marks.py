from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_link_mark import CrmLinkMark
from app.services.crm_link_marks.crm_link_mark_service import CrmLinkMarkService

router = APIRouter(prefix="/crm-link-marks", tags=["crm-link-marks"])

_PERM = "can_manage_crm_link_marks"


class CrmLinkMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    link_kind: str
    source_ref: str


class CrmLinkMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    link_kind: str
    source_ref: str


def _row(saved: CrmLinkMark) -> CrmLinkMarkResponse:
    return CrmLinkMarkResponse.model_validate(saved)


@router.get("", response_model=list[CrmLinkMarkResponse])
async def list_crm_link_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmLinkMarkResponse]:
    packed = await CrmLinkMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CrmLinkMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_link_mark(
    body: CrmLinkMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmLinkMarkResponse:
    saved = await CrmLinkMarkService(session).persist_crm_link_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        link_kind=body.link_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
