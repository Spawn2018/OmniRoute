from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.collaboration_mark import CollaborationMark
from app.services.collaboration_marks.collaboration_mark_service import (
    CollaborationMarkService,
)

router = APIRouter(prefix="/collaboration-marks", tags=["collaboration-marks"])

_PERM = "can_manage_collaboration_marks"


class CollaborationMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    role_kind: str
    source_ref: str


class CollaborationMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    role_kind: str
    source_ref: str


def _as_response(saved: CollaborationMark) -> CollaborationMarkResponse:
    return CollaborationMarkResponse.model_validate(saved)


@router.get("", response_model=list[CollaborationMarkResponse])
async def list_collaboration_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CollaborationMarkResponse]:
    packed = await CollaborationMarkService(session).list_marks()
    return [_as_response(row) for row in packed]


@router.post(
    "",
    response_model=CollaborationMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_collaboration_mark(
    body: CollaborationMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CollaborationMarkResponse:
    saved = await CollaborationMarkService(session).persist_collaboration_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        role_kind=body.role_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
