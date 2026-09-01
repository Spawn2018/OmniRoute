from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.nbp_rate import NbpRate
from app.services.nbp_rates.nbp_rate_service import NbpRateService

router = APIRouter(prefix="/nbp-rates", tags=["nbp-rates"])


class NbpRateCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    currency: str = Field(min_length=3, max_length=3)
    rate_date: date
    mid: str = Field(min_length=1, max_length=32)


class NbpRateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    currency: str
    rate_date: date
    mid: str
    source_ref: str

    @classmethod
    def from_row(cls, row: NbpRate) -> "NbpRateResponse":
        return cls(
            id=row.id,
            organization_id=row.organization_id,
            currency=str(row.currency).strip(),
            rate_date=row.rate_date,
            mid=format(row.mid, "f"),
            source_ref=row.source_ref,
        )


@router.get("", response_model=list[NbpRateResponse])
async def list_nbp_rates(
    _authz: None = Depends(require_permission("can_manage_nbp_rates", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[NbpRateResponse]:
    service = NbpRateService(session)
    rows = await service.list_rates()
    return [NbpRateResponse.from_row(row) for row in rows]


@router.get("/resolve", response_model=NbpRateResponse)
async def resolve_nbp_rate(
    currency: str = Query(..., min_length=3, max_length=3),
    on_date: date = Query(...),
    _authz: None = Depends(require_permission("can_manage_nbp_rates", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> NbpRateResponse:
    service = NbpRateService(session)
    row = await service.resolve(currency, on_date)
    return NbpRateResponse.from_row(row)


@router.post("", response_model=NbpRateResponse, status_code=status.HTTP_201_CREATED)
async def create_nbp_rate(
    body: NbpRateCreate,
    _authz: None = Depends(require_permission("can_manage_nbp_rates", "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> NbpRateResponse:
    service = NbpRateService(session)
    row = await service.create_rate(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        currency=body.currency,
        rate_date=body.rate_date,
        mid=body.mid,
    )
    await session.commit()
    return NbpRateResponse.from_row(row)
