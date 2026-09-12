"""HTTP katalog wipe demo — HITL, bez live wipe i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.demo_wipe_mark import DemoWipeMark
from app.services.demo_wipe_marks.demo_wipe_mark_service import (
    DemoWipeMarkService,
)

router = APIRouter(prefix="/demo-wipe-marks", tags=["demo-wipe-mark"])
_PERM = "can_manage_demo_wipe_marks"


class DemoWipeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    wipe_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class DemoWipeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    wipe_kind: str
    source_ref: str


def _to_dto(row: DemoWipeMark) -> DemoWipeMarkResponse:
    return DemoWipeMarkResponse.model_validate(row)


@router.get("", response_model=list[DemoWipeMarkResponse])
async def list_demo_wipe_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DemoWipeMarkResponse]:
    catalog = DemoWipeMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=DemoWipeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_demo_wipe_mark(
    body: DemoWipeMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DemoWipeMarkResponse:
    catalog = DemoWipeMarkService(session)
    saved = await catalog.persist_demo_wipe_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        wipe_kind=body.wipe_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "demo-wipe-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
