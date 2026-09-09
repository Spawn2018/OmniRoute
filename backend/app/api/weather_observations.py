from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.models.weather_observation import WeatherObservation
from app.services.weather_observations.weather_observation_service import (
    WeatherObservationService,
)

router = APIRouter(prefix="/weather-observations", tags=["weather-observations"])

_PERM = "can_manage_weather_observations"


class WeatherObservationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    condition_code: str
    station_unlocode: str
    observed_at: str
    provider_code: str
    source_ref: str


class WeatherObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    condition_code: str
    station_unlocode: str
    observed_at: datetime
    provider_code: str
    source_ref: str


def _as_row(row: WeatherObservation) -> WeatherObservationResponse:
    return WeatherObservationResponse.model_validate(row)


@router.get("", response_model=list[WeatherObservationResponse])
async def list_weather_observations(
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[WeatherObservationResponse]:
    rows = await WeatherObservationService(session).list_marks()
    return [_as_row(row) for row in rows]


@router.post(
    "",
    response_model=WeatherObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_weather_observation(
    body: WeatherObservationCreate,
    _authz: None = Depends(require_permission(_PERM, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> WeatherObservationResponse:
    row = await WeatherObservationService(session).persist_mark(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        condition_code=body.condition_code,
        station_unlocode=body.station_unlocode,
        observed_at=body.observed_at,
        provider_code=body.provider_code,
        source_ref=body.source_ref,
    )
    await session.commit()
    return _as_row(row)
