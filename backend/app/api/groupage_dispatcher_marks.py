from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.groupage_dispatcher_mark import GroupageDispatcherMark
from app.services.groupage_dispatcher_marks.groupage_dispatcher_mark_service import (
    GroupageDispatcherMarkService,
)

router = APIRouter(prefix="/groupage-dispatcher-marks", tags=["groupage-dispatcher-marks"])

_PERM = "can_manage_groupage_dispatcher_marks"


class GroupageDispatcherMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    dispatcher_kind: str
    source_ref: str


class GroupageDispatcherMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    dispatcher_kind: str
    source_ref: str


def _row(saved: GroupageDispatcherMark) -> GroupageDispatcherMarkResponse:
    return GroupageDispatcherMarkResponse.model_validate(saved)


@router.get("", response_model=list[GroupageDispatcherMarkResponse])
async def list_groupage_dispatcher_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[GroupageDispatcherMarkResponse]:
    packed = await GroupageDispatcherMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=GroupageDispatcherMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_groupage_dispatcher_mark(
    body: GroupageDispatcherMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> GroupageDispatcherMarkResponse:
    saved = await GroupageDispatcherMarkService(session).persist_groupage_dispatcher_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        dispatcher_kind=body.dispatcher_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
