"""HTTP katalog po plant — HITL, bez live EDI i kwoty."""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.po_plant_mark import PoPlantMark
from app.services.po_plant_marks.po_plant_mark_service import (
    PoPlantMarkService,
)

router = APIRouter(prefix="/po-plant-marks", tags=["po-plant-mark"])
_PERM = "can_manage_po_plant_marks"


class PoPlantMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str = Field(min_length=2, max_length=32)
    plant_kind: str = Field(min_length=2, max_length=16)
    source_ref: str = Field(min_length=1, max_length=256)


class PoPlantMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    plant_kind: str
    source_ref: str


def _to_dto(row: PoPlantMark) -> PoPlantMarkResponse:
    return PoPlantMarkResponse.model_validate(row)


@router.get("", response_model=list[PoPlantMarkResponse])
async def list_po_plant_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[PoPlantMarkResponse]:
    catalog = PoPlantMarkService(session)
    return [_to_dto(mark) for mark in await catalog.list_marks()]


@router.post(
    "",
    response_model=PoPlantMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_po_plant_mark(
    body: PoPlantMarkCreate,
    response: Response,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> PoPlantMarkResponse:
    catalog = PoPlantMarkService(session)
    saved = await catalog.persist_po_plant_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        plant_kind=body.plant_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    response.headers["X-Omni-Catalog"] = "po-plant-mark"
    response.headers["X-Omni-Mode"] = "hitl"
    return _to_dto(saved)
