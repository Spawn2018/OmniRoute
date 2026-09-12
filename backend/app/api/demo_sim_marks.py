"""HTTP katalog demo sim — HITL, bez live floty i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.demo_sim_mark import DemoSimMark
from app.services.demo_sim_marks.demo_sim_mark_service import (
    DemoSimMarkService,
)

router = APIRouter(prefix="/demo-sim-marks", tags=["demo-sim-mark"])
_PERM = "can_manage_demo_sim_marks"


class DemoSimMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    sim_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class DemoSimMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    sim_kind: str
    source_ref: str


def _to_dto(row: DemoSimMark) -> DemoSimMarkResponse:
    return DemoSimMarkResponse.model_validate(row)


@router.get("", response_model=list[DemoSimMarkResponse])
async def list_demo_sim_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DemoSimMarkResponse]:
    catalog = DemoSimMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=DemoSimMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_demo_sim_mark(
    body: DemoSimMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DemoSimMarkResponse:
    catalog = DemoSimMarkService(session)
    saved = await catalog.persist_demo_sim_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        sim_kind=body.sim_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "demo-sim-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
