from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.remediation_option import RemediationOption
from app.services.remediation_options.remediation_option_service import (
    RemediationOptionService,
)

router = APIRouter(prefix="/remediation-options", tags=["remediation-options"])

_PERM = "can_manage_remediation_options"


class RemediationOptionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    option_code: str
    option_kind: str
    source_ref: str


class RemediationOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    option_code: str
    option_kind: str
    source_ref: str


def _row(saved: RemediationOption) -> RemediationOptionResponse:
    return RemediationOptionResponse.model_validate(saved)


@router.get("", response_model=list[RemediationOptionResponse])
async def list_remediation_options(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RemediationOptionResponse]:
    packed = await RemediationOptionService(session).list_options()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RemediationOptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_remediation_option(
    body: RemediationOptionCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RemediationOptionResponse:
    saved = await RemediationOptionService(session).persist_remediation_option(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        option_code=body.option_code,
        option_kind=body.option_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
