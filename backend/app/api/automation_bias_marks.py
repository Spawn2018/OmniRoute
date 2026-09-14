from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.automation_bias_mark import AutomationBiasMark
from app.services.automation_bias_marks.automation_bias_mark_service import (
    AutomationBiasMarkService,
)

router = APIRouter(
    prefix="/automation-bias-marks",
    tags=["automation-bias-marks"],
)

_PERM = "can_manage_automation_bias_marks"


class AutomationBiasMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bias_kind: str
    source_ref: str


class AutomationBiasMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bias_kind: str
    source_ref: str


def _row(saved: AutomationBiasMark) -> AutomationBiasMarkResponse:
    return AutomationBiasMarkResponse.model_validate(saved)


@router.get("", response_model=list[AutomationBiasMarkResponse])
async def list_automation_bias_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[AutomationBiasMarkResponse]:
    packed = await AutomationBiasMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=AutomationBiasMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_automation_bias_mark(
    body: AutomationBiasMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> AutomationBiasMarkResponse:
    saved = await AutomationBiasMarkService(session).persist_automation_bias_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bias_kind=body.bias_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
