from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.clone_carry_mark import CloneCarryMark
from app.services.clone_carry_marks.clone_carry_mark_service import (
    CloneCarryMarkService,
)

router = APIRouter(prefix="/clone-carry-marks", tags=["clone-carry-marks"])

_PERM = "can_manage_clone_carry_marks"


class CloneCarryMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    carry_kind: str
    source_ref: str


class CloneCarryMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    carry_kind: str
    source_ref: str


def _as_response(row: CloneCarryMark) -> CloneCarryMarkResponse:
    return CloneCarryMarkResponse.model_validate(row)


@router.get("", response_model=list[CloneCarryMarkResponse])
async def list_clone_carry_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CloneCarryMarkResponse]:
    rows = await CloneCarryMarkService(session).list_marks()
    return [_as_response(row) for row in rows]


@router.post(
    "",
    response_model=CloneCarryMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_clone_carry_mark(
    body: CloneCarryMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CloneCarryMarkResponse:
    saved = await CloneCarryMarkService(session).persist_clone_carry_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        carry_kind=body.carry_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_response(saved)
