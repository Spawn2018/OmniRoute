from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.offboarding_mark import OffboardingMark
from app.services.offboarding_marks.offboarding_mark_service import (
    OffboardingMarkService,
)

router = APIRouter(prefix="/offboarding-marks", tags=["offboarding-marks"])

_PERM = "can_manage_offboarding_marks"


class OffboardingMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    offboard_kind: str
    source_ref: str


class OffboardingMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    offboard_kind: str
    source_ref: str


def _row(saved: OffboardingMark) -> OffboardingMarkResponse:
    return OffboardingMarkResponse.model_validate(saved)


@router.get("", response_model=list[OffboardingMarkResponse])
async def list_offboarding_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OffboardingMarkResponse]:
    packed = await OffboardingMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=OffboardingMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_offboarding_mark(
    body: OffboardingMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OffboardingMarkResponse:
    saved = await OffboardingMarkService(session).persist_offboarding_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        offboard_kind=body.offboard_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
