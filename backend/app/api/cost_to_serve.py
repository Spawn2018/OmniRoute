from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.cost_to_serve.cost_to_serve_service import CostToServeService
from app.services.parties.party_service import PartyService
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/cost-to-serves", tags=["cost-to-serves"])


class CostToServeCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    customer_sop_id: UUID
    quotation_id: UUID
    source_ref: str


class CostToServeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    customer_sop_id: UUID
    quotation_id: UUID
    source_ref: str


@router.get("", response_model=list[CostToServeResponse])
async def list_cost_to_serve(
    _authz: None = Depends(require_permission("can_manage_cost_to_serve", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[CostToServeResponse]:
    rows = await CostToServeService(session).list_rows()
    return [CostToServeResponse.model_validate(row) for row in rows]


@router.post("", response_model=CostToServeResponse, status_code=status.HTTP_201_CREATED)
async def create_cost_to_serve(
    body: CostToServeCreate,
    _authz: None = Depends(require_permission("can_manage_cost_to_serve", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> CostToServeResponse:
    sop = await PartyService(session).get_sop(body.customer_sop_id)
    quotation = await QuotationService(session).get_quotation(body.quotation_id)
    row = await CostToServeService(session).record_row(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        customer_sop_id=sop.id,
        quotation_id=quotation.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return CostToServeResponse.model_validate(row)
