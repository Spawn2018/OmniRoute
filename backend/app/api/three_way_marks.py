"""HTTP katalog 3-way — HITL, bez tuple per strona i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.three_way_mark import ThreeWayMark
from app.services.three_way_marks.three_way_mark_service import (
    ThreeWayMarkService,
)

router = APIRouter(prefix="/three-way-marks", tags=["three-way-mark"])
_PERM = "can_manage_three_way_marks"


class ThreeWayMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    way_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ThreeWayMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    way_kind: str
    source_ref: str


def _to_dto(row: ThreeWayMark) -> ThreeWayMarkResponse:
    return ThreeWayMarkResponse.model_validate(row)


@router.get("", response_model=list[ThreeWayMarkResponse])
async def list_three_way_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ThreeWayMarkResponse]:
    catalog = ThreeWayMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=ThreeWayMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_three_way_mark(
    body: ThreeWayMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ThreeWayMarkResponse:
    catalog = ThreeWayMarkService(session)
    saved = await catalog.persist_three_way_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        way_kind=body.way_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "three-way-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
