"""HTTP katalog chassis/trailer — HITL, bez live pool i TEU."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.chassis_mark import ChassisMark
from app.services.chassis_marks.chassis_mark_service import (
    ChassisMarkService,
)

router = APIRouter(prefix="/chassis-marks", tags=["chassis-mark"])
_PERM = "can_manage_chassis_marks"


class ChassisMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    chassis_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class ChassisMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    chassis_kind: str
    source_ref: str


def _to_dto(row: ChassisMark) -> ChassisMarkResponse:
    return ChassisMarkResponse.model_validate(row)


@router.get("", response_model=list[ChassisMarkResponse])
async def list_chassis_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ChassisMarkResponse]:
    catalog = ChassisMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=ChassisMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chassis_mark(
    body: ChassisMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ChassisMarkResponse:
    catalog = ChassisMarkService(session)
    saved = await catalog.persist_chassis_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        chassis_kind=body.chassis_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "chassis-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
