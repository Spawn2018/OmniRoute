"""HTTP katalog demo GPS — HITL, bez live poll i lat/lng."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.demo_gps_mark import DemoGpsMark
from app.services.demo_gps_marks.demo_gps_mark_service import DemoGpsMarkService

router = APIRouter(prefix="/demo-gps-marks", tags=["demo-gps-mark"])
_PERM = "can_manage_demo_gps_marks"


class DemoGpsMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    demo_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class DemoGpsMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    demo_kind: str
    source_ref: str


def _to_dto(row: DemoGpsMark) -> DemoGpsMarkResponse:
    return DemoGpsMarkResponse.model_validate(row)


@router.get("", response_model=list[DemoGpsMarkResponse])
async def list_demo_gps_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DemoGpsMarkResponse]:
    catalog = DemoGpsMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=DemoGpsMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_demo_gps_mark(
    body: DemoGpsMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DemoGpsMarkResponse:
    catalog = DemoGpsMarkService(session)
    saved = await catalog.persist_demo_gps_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        demo_kind=body.demo_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "demo-gps-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
