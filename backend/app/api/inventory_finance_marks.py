from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.inventory_finance_mark import InventoryFinanceMark
from app.services.inventory_finance_marks.inventory_finance_mark_service import (
    InventoryFinanceMarkService,
)

router = APIRouter(prefix="/inventory-finance-marks", tags=["inventory-finance-marks"])

_PERM = "can_manage_inventory_finance_marks"


class InventoryFinanceMarkCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mark_code: str
    finance_kind: str
    source_ref: str


class InventoryFinanceMarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    mark_code: str
    finance_kind: str
    source_ref: str


def _row(saved: InventoryFinanceMark) -> InventoryFinanceMarkResponse:
    return InventoryFinanceMarkResponse.model_validate(saved)


@router.get("", response_model=list[InventoryFinanceMarkResponse])
async def list_inventory_finance_marks(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[InventoryFinanceMarkResponse]:
    packed = await InventoryFinanceMarkService(session).list_marks()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=InventoryFinanceMarkResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_inventory_finance_mark(
    body: InventoryFinanceMarkCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> InventoryFinanceMarkResponse:
    saved = await InventoryFinanceMarkService(session).persist_inventory_finance_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        mark_code=body.mark_code,
        finance_kind=body.finance_kind,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
