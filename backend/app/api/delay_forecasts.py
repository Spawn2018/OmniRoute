from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.delay_forecast import DelayForecast
from app.services.delay_forecasts.delay_forecast_service import DelayForecastService

router = APIRouter(prefix="/delay-forecasts", tags=["delay-forecasts"])

_PERM = "can_manage_delay_forecasts"


class DelayForecastCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    forecast_code: str
    horizon_hours: int
    p_late: Decimal
    source_ref: str


class DelayForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    forecast_code: str
    horizon_hours: int
    p_late: Decimal
    source_ref: str


def _row(saved: DelayForecast) -> DelayForecastResponse:
    return DelayForecastResponse.model_validate(saved)


@router.get("", response_model=list[DelayForecastResponse])
async def list_delay_forecasts(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[DelayForecastResponse]:
    packed = await DelayForecastService(session).list_forecasts()
    return [_row(item) for item in packed]


@router.post(
    "",
    response_model=DelayForecastResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_delay_forecast(
    body: DelayForecastCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> DelayForecastResponse:
    saved = await DelayForecastService(session).persist_delay_forecast(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        forecast_code=body.forecast_code,
        horizon_hours=body.horizon_hours,
        p_late=body.p_late,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _row(saved)
