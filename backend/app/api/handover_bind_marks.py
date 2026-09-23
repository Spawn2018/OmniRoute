from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.handover_bind_mark import HandoverBindMark
from app.services.handover_bind_marks.handover_bind_mark_service import (
    HandoverBindMarkService,
)

router = APIRouter(
    prefix="/handover-bind-marks",
    tags=["handover-bind-marks"],
)

_PERM = "can_manage_handover_bind_marks"


class HandoverBindMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    bind_kind: str
    source_ref: str


class HandoverBindMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    bind_kind: str
    source_ref: str


def _as_response(row: HandoverBindMark) -> HandoverBindMarkResponse:
    return HandoverBindMarkResponse.model_validate(row)


@router.get("", response_model=list[HandoverBindMarkResponse])
async def list_handover_bind_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[HandoverBindMarkResponse]:
    rows = await HandoverBindMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=HandoverBindMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_handover_bind_mark(
    body: HandoverBindMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> HandoverBindMarkResponse:
    saved = await HandoverBindMarkService(session).persist_handover_bind_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        bind_kind=body.bind_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
