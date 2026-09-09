from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.memory_edge import MemoryEdge
from app.services.memory_edges.memory_edge_service import MemoryEdgeService

router = APIRouter(prefix="/memory-edges", tags=["memory-edges"])

_PERM = "can_manage_memory_edges"


class MemoryEdgeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_kind: str
    source_ref: str


class MemoryEdgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    edge_kind: str
    source_ref: str


def _as_row(row: MemoryEdge) -> MemoryEdgeResponse:
    return MemoryEdgeResponse.model_validate(row)


@router.get("", response_model=list[MemoryEdgeResponse])
async def list_memory_edges(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[MemoryEdgeResponse]:
    rows = await MemoryEdgeService(session).list_links()
    return [_as_row(row) for row in rows]


@router.post("", response_model=MemoryEdgeResponse, status_code=status.HTTP_201_CREATED)
async def create_memory_edge(
    body: MemoryEdgeCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> MemoryEdgeResponse:
    row = await MemoryEdgeService(session).record_link(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        edge_kind=body.edge_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
