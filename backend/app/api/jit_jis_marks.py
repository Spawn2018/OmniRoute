from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.jit_jis_mark import JitJisMark
from app.services.jit_jis_marks.jit_jis_mark_service import (
    JitJisMarkService,
)

router = APIRouter(prefix="/jit-jis-marks", tags=["jit-jis-marks"])

_PERM = "can_manage_jit_jis_marks"


class JitJisMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    flow_kind: str
    source_ref: str


class JitJisMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    flow_kind: str
    source_ref: str


def _row(saved: JitJisMark) -> JitJisMarkResponse:
    return JitJisMarkResponse.model_validate(saved)


@router.get("", response_model=list[JitJisMarkResponse])
async def list_jit_jis_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[JitJisMarkResponse]:
    packed = await JitJisMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=JitJisMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_jit_jis_mark(
    body: JitJisMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> JitJisMarkResponse:
    saved = await JitJisMarkService(session).persist_jit_jis_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        flow_kind=body.flow_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
