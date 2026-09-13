from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_opportunity import CrmOpportunity
from app.services.crm_opportunities.crm_opportunity_service import CrmOpportunityService

router = APIRouter(prefix="/crm-opportunities", tags=["crm-opportunities"])

_PERM = "can_manage_crm_opportunities"


class CrmOpportunityCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    opportunity_code: str
    stage_kind: str
    source_ref: str


class CrmOpportunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    opportunity_code: str
    stage_kind: str
    source_ref: str


def _row(saved: CrmOpportunity) -> CrmOpportunityResponse:
    return CrmOpportunityResponse.model_validate(saved)


@router.get("", response_model=list[CrmOpportunityResponse])
async def list_crm_opportunities(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmOpportunityResponse]:
    packed = await CrmOpportunityService(session).list_opportunities()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CrmOpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_opportunity(
    body: CrmOpportunityCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmOpportunityResponse:
    saved = await CrmOpportunityService(session).persist_crm_opportunity(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        opportunity_code=body.opportunity_code,
        stage_kind=body.stage_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
