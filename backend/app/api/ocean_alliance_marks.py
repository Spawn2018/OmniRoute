"""HTTP katalog ocean alliance — HITL, bez live filing."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.ocean_alliance_mark import OceanAllianceMark
from app.services.ocean_alliance_marks.ocean_alliance_mark_service import OceanAllianceMarkService

router = APIRouter(prefix="/ocean-alliance-marks", tags=["ocean-alliance"])

_PERM = "can_manage_ocean_alliance_marks"


class OceanAllianceMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    ocean_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class OceanAllianceMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    ocean_kind: str
    source_ref: str


def _to_dto(row: OceanAllianceMark) -> OceanAllianceMarkResponse:
    return OceanAllianceMarkResponse.model_validate(row)


@router.get("", response_model=list[OceanAllianceMarkResponse])
async def list_ocean_alliance_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[OceanAllianceMarkResponse]:
    catalog = OceanAllianceMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post("", response_model=OceanAllianceMarkResponse, status_code=status.HTTP_201_CREATED)
async def create_ocean_alliance_mark(
    body: OceanAllianceMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> OceanAllianceMarkResponse:
    catalog = OceanAllianceMarkService(session)
    saved = await catalog.persist_ocean_alliance_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        ocean_kind=body.ocean_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "ocean-alliance-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
