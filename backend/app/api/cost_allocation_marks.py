from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cost_allocation_mark import CostAllocationMark
from app.services.cost_allocation_marks.cost_allocation_mark_service import (
    CostAllocationMarkService,
)

router = APIRouter(prefix="/cost-allocation-marks", tags=["cost-allocation-marks"])

_PERM = "can_manage_cost_allocation_marks"


class CostAllocationMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    alloc_kind: str
    source_ref: str


class CostAllocationMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    alloc_kind: str
    source_ref: str


def _row(saved: CostAllocationMark) -> CostAllocationMarkResponse:
    return CostAllocationMarkResponse.model_validate(saved)


@router.get("", response_model=list[CostAllocationMarkResponse])
async def list_cost_allocation_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CostAllocationMarkResponse]:
    packed = await CostAllocationMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CostAllocationMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cost_allocation_mark(
    body: CostAllocationMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CostAllocationMarkResponse:
    saved = await CostAllocationMarkService(session).persist_cost_allocation_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        alloc_kind=body.alloc_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
