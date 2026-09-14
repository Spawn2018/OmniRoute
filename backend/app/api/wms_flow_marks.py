from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.wms_flow_mark import WmsFlowMark
from app.services.wms_flow_marks.wms_flow_mark_service import WmsFlowMarkService

router = APIRouter(prefix="/wms-flow-marks", tags=["wms-flow-marks"])

_PERM = "can_manage_wms_flow_marks"


class WmsFlowMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    flow_kind: str
    source_ref: str


class WmsFlowMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    flow_kind: str
    source_ref: str


def _row(saved: WmsFlowMark) -> WmsFlowMarkResponse:
    return WmsFlowMarkResponse.model_validate(saved)


@router.get("", response_model=list[WmsFlowMarkResponse])
async def list_wms_flow_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WmsFlowMarkResponse]:
    packed = await WmsFlowMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=WmsFlowMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wms_flow_mark(
    body: WmsFlowMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WmsFlowMarkResponse:
    saved = await WmsFlowMarkService(session).persist_wms_flow_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        flow_kind=body.flow_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
