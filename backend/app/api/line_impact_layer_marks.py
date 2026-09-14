from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.line_impact_layer_mark import LineImpactLayerMark
from app.services.line_impact_layer_marks.line_impact_layer_mark_service import (
    LineImpactLayerMarkService,
)

router = APIRouter(
    prefix="/line-impact-layer-marks",
    tags=["line-impact-layer-marks"],
)

_PERM = "can_manage_line_impact_layer_marks"


class LineImpactLayerMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    layer_kind: str
    source_ref: str


class LineImpactLayerMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    layer_kind: str
    source_ref: str


def _row(saved: LineImpactLayerMark) -> LineImpactLayerMarkResponse:
    return LineImpactLayerMarkResponse.model_validate(saved)


@router.get("", response_model=list[LineImpactLayerMarkResponse])
async def list_line_impact_layer_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[LineImpactLayerMarkResponse]:
    packed = await LineImpactLayerMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=LineImpactLayerMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_line_impact_layer_mark(
    body: LineImpactLayerMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> LineImpactLayerMarkResponse:
    saved = await LineImpactLayerMarkService(session).persist_line_impact_layer_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        layer_kind=body.layer_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
