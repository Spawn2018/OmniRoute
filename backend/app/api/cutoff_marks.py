from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cutoff_mark import CutoffMark
from app.services.cutoff_marks.cutoff_mark_service import (
    CutoffMarkService,
)

router = APIRouter(prefix="/cutoff-marks", tags=["cutoff-marks"])

_PERM = "can_manage_cutoff_marks"


class CutoffMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    cutoff_kind: str
    source_ref: str


class CutoffMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    cutoff_kind: str
    source_ref: str


def _row(saved: CutoffMark) -> CutoffMarkResponse:
    return CutoffMarkResponse.model_validate(saved)


@router.get("", response_model=list[CutoffMarkResponse])
async def list_cutoff_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CutoffMarkResponse]:
    packed = await CutoffMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CutoffMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cutoff_mark(
    body: CutoffMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CutoffMarkResponse:
    saved = await CutoffMarkService(session).persist_cutoff_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        cutoff_kind=body.cutoff_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
