from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.services.fx_differences.fx_difference_service import FxDifferenceService
from app.services.nbp_rates.nbp_rate_service import NbpRateService
from app.services.quotations.quotation_service import QuotationService

router = APIRouter(prefix="/fx-differences", tags=["fx-differences"])


class FxDifferenceCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    quotation_id: UUID
    nbp_rate_id: UUID
    source_ref: str


class FxDifferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    quotation_id: UUID
    nbp_rate_id: UUID
    source_ref: str


@router.get("", response_model=list[FxDifferenceResponse])
async def list_fx_differences(
    _authz: None = Depends(require_permission("can_manage_fx_differences", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[FxDifferenceResponse]:
    rows = await FxDifferenceService(session).list_differences()
    return [FxDifferenceResponse.model_validate(row) for row in rows]


@router.post("", response_model=FxDifferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_fx_difference(
    body: FxDifferenceCreate,
    _authz: None = Depends(require_permission("can_manage_fx_differences", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> FxDifferenceResponse:
    quotation = await QuotationService(session).get_quotation(body.quotation_id)
    rate = await NbpRateService(session).get_rate(body.nbp_rate_id)
    row = await FxDifferenceService(session).record_difference(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        quotation_id=quotation.id,
        nbp_rate_id=rate.id,
        source_ref=body.source_ref,
    )
    await session.commit()
    return FxDifferenceResponse.model_validate(row)
