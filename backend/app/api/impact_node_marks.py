from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.impact_node_mark import ImpactNodeMark
from app.services.impact_node_marks.impact_node_mark_service import (
    ImpactNodeMarkService,
)

router = APIRouter(prefix="/impact-node-marks", tags=["impact-node-marks"])

_PERM = "can_manage_impact_node_marks"


class ImpactNodeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    node_kind: str
    source_ref: str


class ImpactNodeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    node_kind: str
    source_ref: str


def _row(saved: ImpactNodeMark) -> ImpactNodeMarkResponse:
    return ImpactNodeMarkResponse.model_validate(saved)


@router.get("", response_model=list[ImpactNodeMarkResponse])
async def list_impact_node_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[ImpactNodeMarkResponse]:
    packed = await ImpactNodeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=ImpactNodeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_impact_node_mark(
    body: ImpactNodeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> ImpactNodeMarkResponse:
    saved = await ImpactNodeMarkService(session).persist_impact_node_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        node_kind=body.node_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
