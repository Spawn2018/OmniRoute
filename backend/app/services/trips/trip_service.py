from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.trip import (
    require_trip_no,
    require_trip_resource_id,
    require_trip_source_ref,
    require_trip_status,
)
from app.models.trip import Trip
from app.repositories.trips.trip_repository import TripRepository


class _RunDraft(NamedTuple):
    number: str
    state: str
    vehicle_id: UUID | None
    trailer_id: UUID | None
    driver_id: UUID | None
    origin: str


def _run_draft(
    trip_no: object,
    status: object,
    vehicle_id: object,
    trailer_id: object,
    driver_id: object,
    source_ref: object,
) -> _RunDraft:
    return _RunDraft(
        require_trip_no(trip_no),
        require_trip_status(status),
        require_trip_resource_id(vehicle_id),
        require_trip_resource_id(trailer_id),
        require_trip_resource_id(driver_id),
        require_trip_source_ref(source_ref),
    )


def _run_unchanged(current: Trip, draft: _RunDraft) -> bool:
    return (
        current.status == draft.state
        and current.vehicle_id == draft.vehicle_id
        and current.trailer_id == draft.trailer_id
        and current.driver_id == draft.driver_id
        and current.source_ref == draft.origin
    )


class TripService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TripRepository(session)

    async def list_trips(self, *, status: object | None = None) -> list[Trip]:
        state = None if status is None else require_trip_status(status)
        return await self._rows.list_current(state)

    async def record_trip(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        trip_no: object,
        status: object,
        vehicle_id: object,
        trailer_id: object,
        driver_id: object,
        source_ref: object,
    ) -> Trip:
        draft = _run_draft(trip_no, status, vehicle_id, trailer_id, driver_id, source_ref)
        current = await self._rows.find_current(draft.number)
        if current is not None and _run_unchanged(current, draft):
            return current
        saved = await self._rows.add(
            Trip(
                id=uuid4(),
                organization_id=organization_id,
                trip_no=draft.number,
                status=draft.state,
                vehicle_id=draft.vehicle_id,
                trailer_id=draft.trailer_id,
                driver_id=draft.driver_id,
                source_ref=draft.origin,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved
