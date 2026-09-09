from decimal import Decimal
from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.trip import (
    require_distinct_drivers,
    require_expected_buy,
    require_route_label,
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
    driver2_id: UUID | None
    origin: str
    route_label: str | None
    buy_amount: Decimal | None
    buy_currency: str | None


def _run_draft(
    trip_no: object,
    status: object,
    vehicle_id: object,
    trailer_id: object,
    driver_id: object,
    driver2_id: object,
    source_ref: object,
    expected_buy_amount: object,
    expected_buy_currency: object,
    route_label: object,
) -> _RunDraft:
    state = require_trip_status(status)
    buy_amount, buy_currency = require_expected_buy(
        state,
        expected_buy_amount,
        expected_buy_currency,
    )
    first = require_trip_resource_id(driver_id)
    second = require_trip_resource_id(driver2_id)
    require_distinct_drivers(first, second)
    return _RunDraft(
        require_trip_no(trip_no),
        state,
        require_trip_resource_id(vehicle_id),
        require_trip_resource_id(trailer_id),
        first,
        second,
        require_trip_source_ref(source_ref),
        require_route_label(route_label),
        buy_amount,
        buy_currency,
    )


def _run_unchanged(current: Trip, draft: _RunDraft) -> bool:
    return (
        current.status == draft.state
        and current.vehicle_id == draft.vehicle_id
        and current.trailer_id == draft.trailer_id
        and current.driver_id == draft.driver_id
        and current.driver2_id == draft.driver2_id
        and current.source_ref == draft.origin
        and current.route_label == draft.route_label
        and current.expected_buy_amount == draft.buy_amount
        and (
            None
            if current.expected_buy_currency is None
            else str(current.expected_buy_currency).strip()
        )
        == draft.buy_currency
    )


class TripService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = TripRepository(session)

    async def list_trips(self, *, status: object | None = None) -> list[Trip]:
        state = None if status is None else require_trip_status(status)
        return await self._rows.list_current(state)

    async def _persist_run(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        draft: _RunDraft,
        current: Trip | None,
    ) -> Trip:
        saved = await self._rows.add(
            Trip(
                id=uuid4(),
                organization_id=organization_id,
                trip_no=draft.number,
                status=draft.state,
                vehicle_id=draft.vehicle_id,
                trailer_id=draft.trailer_id,
                driver_id=draft.driver_id,
                driver2_id=draft.driver2_id,
                source_ref=draft.origin,
                route_label=draft.route_label,
                expected_buy_amount=draft.buy_amount,
                expected_buy_currency=draft.buy_currency,
                created_by=user_id,
            ),
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

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
        expected_buy_amount: object = None,
        expected_buy_currency: object = None,
        driver2_id: object = None,
        route_label: object = None,
    ) -> Trip:
        draft = _run_draft(
            trip_no,
            status,
            vehicle_id,
            trailer_id,
            driver_id,
            driver2_id,
            source_ref,
            expected_buy_amount,
            expected_buy_currency,
            route_label,
        )
        current = await self._rows.find_current(draft.number)
        if current is not None and _run_unchanged(current, draft):
            return current
        return await self._persist_run(
            organization_id=organization_id,
            user_id=user_id,
            draft=draft,
            current=current,
        )
