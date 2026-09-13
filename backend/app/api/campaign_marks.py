from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.campaign_mark import CampaignMark
from app.services.campaign_marks.campaign_mark_service import CampaignMarkService

router = APIRouter(prefix="/campaign-marks", tags=["campaign-marks"])

_PERM = "can_manage_campaign_marks"


class CampaignMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    campaign_kind: str
    source_ref: str


class CampaignMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    campaign_kind: str
    source_ref: str


def _row(saved: CampaignMark) -> CampaignMarkResponse:
    return CampaignMarkResponse.model_validate(saved)


@router.get("", response_model=list[CampaignMarkResponse])
async def list_campaign_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CampaignMarkResponse]:
    packed = await CampaignMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CampaignMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_campaign_mark(
    body: CampaignMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CampaignMarkResponse:
    saved = await CampaignMarkService(session).persist_campaign_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        campaign_kind=body.campaign_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
