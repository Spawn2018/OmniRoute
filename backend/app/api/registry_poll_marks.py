from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.registry_poll_mark import RegistryPollMark
from app.services.registry_poll_marks.registry_poll_mark_service import RegistryPollMarkService

router = APIRouter(prefix="/registry-poll-marks", tags=["registry-poll-marks"])

_PERM = "can_manage_registry_poll_marks"


class RegistryPollMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    poll_kind: str
    source_ref: str


class RegistryPollMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    poll_kind: str
    source_ref: str


def _row(saved: RegistryPollMark) -> RegistryPollMarkResponse:
    return RegistryPollMarkResponse.model_validate(saved)


@router.get("", response_model=list[RegistryPollMarkResponse])
async def list_registry_poll_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RegistryPollMarkResponse]:
    packed = await RegistryPollMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=RegistryPollMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_registry_poll_mark(
    body: RegistryPollMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RegistryPollMarkResponse:
    saved = await RegistryPollMarkService(session).persist_registry_poll_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        poll_kind=body.poll_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
