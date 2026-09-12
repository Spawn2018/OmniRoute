"""HTTP katalog UIC/CIM/SMGS — HITL, bez live rail API i km."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.rail_uic_mark import RailUicMark
from app.services.rail_uic_marks.rail_uic_mark_service import (
    RailUicMarkService,
)

router = APIRouter(prefix="/rail-uic-marks", tags=["rail-uic-mark"])
_PERM = "can_manage_rail_uic_marks"


class RailUicMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    rail_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class RailUicMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    rail_kind: str
    source_ref: str


def _to_dto(row: RailUicMark) -> RailUicMarkResponse:
    return RailUicMarkResponse.model_validate(row)


@router.get("", response_model=list[RailUicMarkResponse])
async def list_rail_uic_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[RailUicMarkResponse]:
    catalog = RailUicMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=RailUicMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_rail_uic_mark(
    body: RailUicMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> RailUicMarkResponse:
    catalog = RailUicMarkService(session)
    saved = await catalog.persist_rail_uic_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        rail_kind=body.rail_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "rail-uic-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
