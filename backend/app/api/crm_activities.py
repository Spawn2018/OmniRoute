from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_activity import CrmActivity
from app.services.crm_activities.crm_activity_service import CrmActivityService

router = APIRouter(prefix="/crm-activities", tags=["crm-activities"])

_PERM = "can_manage_crm_activities"


class CrmActivityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity_code: str
    activity_kind: str
    source_ref: str


class CrmActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    activity_code: str
    activity_kind: str
    source_ref: str


def _row(saved: CrmActivity) -> CrmActivityResponse:
    return CrmActivityResponse.model_validate(saved)


@router.get("", response_model=list[CrmActivityResponse])
async def list_crm_activities(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmActivityResponse]:
    packed = await CrmActivityService(session).list_activities()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CrmActivityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_activity(
    body: CrmActivityCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmActivityResponse:
    saved = await CrmActivityService(session).persist_crm_activity(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        activity_code=body.activity_code,
        activity_kind=body.activity_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
