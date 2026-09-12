"""HTTP katalog segregacji UN — HITL, bez solver OR i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.un_segregation_mark import UnSegregationMark
from app.services.un_segregation_marks.un_segregation_mark_service import (
    UnSegregationMarkService,
)

router = APIRouter(prefix="/un-segregation-marks", tags=["un-segregation-mark"])
_PERM = "can_manage_un_segregation_marks"


class UnSegregationMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    segregate_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class UnSegregationMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    segregate_kind: str
    source_ref: str


def _to_dto(row: UnSegregationMark) -> UnSegregationMarkResponse:
    return UnSegregationMarkResponse.model_validate(row)


@router.get("", response_model=list[UnSegregationMarkResponse])
async def list_un_segregation_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[UnSegregationMarkResponse]:
    catalog = UnSegregationMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=UnSegregationMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_un_segregation_mark(
    body: UnSegregationMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> UnSegregationMarkResponse:
    catalog = UnSegregationMarkService(session)
    saved = await catalog.persist_un_segregation_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        segregate_kind=body.segregate_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "un-segregation-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
