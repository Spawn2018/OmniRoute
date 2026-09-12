"""HTTP katalog feeder/short-sea — HITL, bez live feeder i TEU."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ocean_feeder_mark import OceanFeederMark
from app.services.ocean_feeder_marks.ocean_feeder_mark_service import (
    OceanFeederMarkService,
)

router = APIRouter(prefix="/ocean-feeder-marks", tags=["ocean-feeder-mark"])
_PERM = "can_manage_ocean_feeder_marks"


class OceanFeederMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    feeder_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class OceanFeederMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    feeder_kind: str
    source_ref: str


def _to_dto(row: OceanFeederMark) -> OceanFeederMarkResponse:
    return OceanFeederMarkResponse.model_validate(row)


@router.get("", response_model=list[OceanFeederMarkResponse])
async def list_ocean_feeder_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OceanFeederMarkResponse]:
    catalog = OceanFeederMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=OceanFeederMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_ocean_feeder_mark(
    body: OceanFeederMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OceanFeederMarkResponse:
    catalog = OceanFeederMarkService(session)
    saved = await catalog.persist_ocean_feeder_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        feeder_kind=body.feeder_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "ocean-feeder-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
