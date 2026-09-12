"""HTTP katalog widoku roli — HITL, bez board T6 i mapy."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.role_view_mark import RoleViewMark
from app.services.role_view_marks.role_view_mark_service import RoleViewMarkService

router = APIRouter(prefix="/role-view-marks", tags=["role-view"])

_PERM = "can_manage_role_view_marks"


class RoleViewMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    view_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class RoleViewMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    view_kind: str
    source_ref: str


def _to_dto(row: RoleViewMark) -> RoleViewMarkResponse:
    return RoleViewMarkResponse.model_validate(row)


@router.get("", response_model=list[RoleViewMarkResponse])
async def list_role_view_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RoleViewMarkResponse]:
    catalog = RoleViewMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=RoleViewMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_role_view_mark(
    body: RoleViewMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RoleViewMarkResponse:
    catalog = RoleViewMarkService(session)
    saved = await catalog.persist_role_view_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        view_kind=body.view_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "role-view-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
