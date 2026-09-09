from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.weather_observation import (
    require_condition_code,
    require_observed_at,
    require_provider_code,
    require_station_unlocode,
    require_weather_source_ref,
)
from app.models.weather_observation import WeatherObservation
from app.repositories.weather_observations.weather_observation_repository import (
    WeatherObservationRepository,
)


class WeatherObservationService:
    def __init__(self, session: AsyncSession) -> None:
        self._marks = WeatherObservationRepository(session)

    async def list_marks(self) -> list[WeatherObservation]:
        return await self._marks.fetch_marks()

    async def persist_mark(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        condition_code: object,
        station_unlocode: object,
        observed_at: object,
        provider_code: object,
        source_ref: object,
    ) -> WeatherObservation:
        row = WeatherObservation(
            id=uuid4(),
            organization_id=organization_id,
            condition_code=require_condition_code(condition_code),
            station_unlocode=require_station_unlocode(station_unlocode),
            observed_at=require_observed_at(observed_at),
            provider_code=require_provider_code(provider_code),
            source_ref=require_weather_source_ref(source_ref),
            created_by=user_id,
        )
        return await self._marks.add(row)
