from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.integration_hub_mark import IntegrationHubMark
from app.services.integration_hub_marks.integration_hub_mark_service import (
    IntegrationHubMarkService,
)

router = APIRouter(prefix="/integration-hub-marks", tags=["integration-hub-marks"])

_PERM = "can_manage_integration_hub_marks"


class IntegrationHubMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    hub_kind: str
    source_ref: str


class IntegrationHubMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    hub_kind: str
    source_ref: str


def _row(saved: IntegrationHubMark) -> IntegrationHubMarkResponse:
    return IntegrationHubMarkResponse.model_validate(saved)


@router.get("", response_model=list[IntegrationHubMarkResponse])
async def list_integration_hub_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[IntegrationHubMarkResponse]:
    packed = await IntegrationHubMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=IntegrationHubMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_integration_hub_mark(
    body: IntegrationHubMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> IntegrationHubMarkResponse:
    saved = await IntegrationHubMarkService(session).persist_integration_hub_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        hub_kind=body.hub_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
