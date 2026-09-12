"""HTTP katalog reefer — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.multi_manning_mark import MultiManningMark
from app.services.multi_manning_marks.multi_manning_mark_service import MultiManningMarkService

router = APIRouter(prefix="/multi-manning-marks", tags=["empty-depot"])

_PERM = "can_manage_multi_manning_marks"


class MultiManningMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    manning_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class MultiManningMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    manning_kind: str
    source_ref: str


def _to_dto(row: MultiManningMark) -> MultiManningMarkResponse:
    return MultiManningMarkResponse.model_validate(row)


@router.get("", response_model=list[MultiManningMarkResponse])
async def list_multi_manning_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MultiManningMarkResponse]:
    catalog = MultiManningMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=MultiManningMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_multi_manning_mark(
    body: MultiManningMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MultiManningMarkResponse:
    catalog = MultiManningMarkService(session)
    saved = await catalog.persist_multi_manning_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        manning_kind=body.manning_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "multi-manning-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
