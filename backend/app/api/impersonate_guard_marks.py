"""HTTP katalog impersonate guard — HITL, bez unwrap i Auth0 live."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.impersonate_guard_mark import ImpersonateGuardMark
from app.services.impersonate_guard_marks.impersonate_guard_mark_service import (
    ImpersonateGuardMarkService,
)

router = APIRouter(prefix="/impersonate-guard-marks", tags=["impersonate-guard-mark"])
_PERM = "can_manage_impersonate_guard_marks"


class ImpersonateGuardMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    guard_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ImpersonateGuardMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    guard_kind: str
    source_ref: str


def _to_dto(row: ImpersonateGuardMark) -> ImpersonateGuardMarkResponse:
    return ImpersonateGuardMarkResponse.model_validate(row)


@router.get("", response_model=list[ImpersonateGuardMarkResponse])
async def list_impersonate_guard_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ImpersonateGuardMarkResponse]:
    catalog = ImpersonateGuardMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=ImpersonateGuardMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_impersonate_guard_mark(
    body: ImpersonateGuardMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ImpersonateGuardMarkResponse:
    catalog = ImpersonateGuardMarkService(session)
    saved = await catalog.persist_impersonate_guard_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        guard_kind=body.guard_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "impersonate-guard-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
