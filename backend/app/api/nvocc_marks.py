"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.nvocc_mark import NvoccMark
from app.services.nvocc_marks.nvocc_mark_service import NvoccMarkService

router = APIRouter(prefix="/nvocc-marks", tags=["empty-depot"])

_PERM = "can_manage_nvocc_marks"


class NvoccMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    nvocc_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class NvoccMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    nvocc_kind: str
    source_ref: str


def _to_dto(row: NvoccMark) -> NvoccMarkResponse:
    return NvoccMarkResponse.model_validate(row)


@router.get("", response_model=list[NvoccMarkResponse])
async def list_nvocc_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NvoccMarkResponse]:
    catalog = NvoccMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=NvoccMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_nvocc_mark(
    body: NvoccMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NvoccMarkResponse:
    catalog = NvoccMarkService(session)
    saved = await catalog.persist_nvocc_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        nvocc_kind=body.nvocc_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "nvocc-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
