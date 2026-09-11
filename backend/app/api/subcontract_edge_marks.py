from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.subcontract_edge_mark import SubcontractEdgeMark
from app.services.subcontract_edge_marks.subcontract_edge_mark_service import (
    SubcontractEdgeMarkService,
)

router = APIRouter(prefix="/subcontract-edge-marks", tags=["subcontract-edge-marks"])

_PERM = "can_manage_subcontract_edge_marks"


class SubcontractEdgeMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    edge_kind: str
    source_ref: str


class SubcontractEdgeMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    edge_kind: str
    source_ref: str


def _row(saved: SubcontractEdgeMark) -> SubcontractEdgeMarkResponse:
    return SubcontractEdgeMarkResponse.model_validate(saved)


@router.get("", response_model=list[SubcontractEdgeMarkResponse])
async def list_subcontract_edge_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[SubcontractEdgeMarkResponse]:
    packed = await SubcontractEdgeMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=SubcontractEdgeMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subcontract_edge_mark(
    body: SubcontractEdgeMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> SubcontractEdgeMarkResponse:
    saved = await SubcontractEdgeMarkService(session).persist_subcontract_edge_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        edge_kind=body.edge_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
