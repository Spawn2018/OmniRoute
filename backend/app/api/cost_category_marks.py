from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.cost_category_mark import CostCategoryMark
from app.services.cost_category_marks.cost_category_mark_service import (
    CostCategoryMarkService,
)

router = APIRouter(prefix="/cost-category-marks", tags=["cost-category-marks"])

_PERM = "can_manage_cost_category_marks"


class CostCategoryMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    category_kind: str
    source_ref: str


class CostCategoryMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    category_kind: str
    source_ref: str


def _row(saved: CostCategoryMark) -> CostCategoryMarkResponse:
    return CostCategoryMarkResponse.model_validate(saved)


@router.get("", response_model=list[CostCategoryMarkResponse])
async def list_cost_category_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CostCategoryMarkResponse]:
    packed = await CostCategoryMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=CostCategoryMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_cost_category_mark(
    body: CostCategoryMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CostCategoryMarkResponse:
    saved = await CostCategoryMarkService(session).persist_cost_category_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        category_kind=body.category_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
