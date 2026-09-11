from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.crm_lead import CrmLead
from app.services.crm_leads.crm_lead_service import CrmLeadService

router = APIRouter(prefix="/crm-leads", tags=["crm-leads"])

_PERM = "can_manage_crm_leads"


class CrmLeadCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lead_code: str
    stage_kind: str
    source_ref: str


class CrmLeadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    lead_code: str
    stage_kind: str
    source_ref: str


def _lead(saved: CrmLead) -> CrmLeadResponse:
    return CrmLeadResponse.model_validate(saved)


@router.get("", response_model=list[CrmLeadResponse])
async def list_crm_leads(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CrmLeadResponse]:
    packed = await CrmLeadService(session).list_leads()
    return [_lead(item) for item in packed]


@router.post(
    "",
    response_model=CrmLeadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_crm_lead(
    body: CrmLeadCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CrmLeadResponse:
    saved = await CrmLeadService(session).persist_crm_lead(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        lead_code=body.lead_code,
        stage_kind=body.stage_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _lead(saved)
