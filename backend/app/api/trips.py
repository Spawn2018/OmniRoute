from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_identity, require_permission, require_tenant_session
from app.core.session_token import SessionIdentity
from app.domain.trip import require_trip_slot
from app.models.trip import Trip
from app.services.resources.resource_service import ResourceService
from app.services.trips.trip_service import TripService

router = APIRouter(prefix="/trips", tags=["trips"])

_SHIP = "can_manage_shipments"


class TripCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    trip_no: str
    status: str
    vehicle_id: UUID | None = None
    trailer_id: UUID | None = None
    driver_id: UUID | None = None
    source_ref: str
    expected_buy_amount: str | None = None
    expected_buy_currency: str | None = None


class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    organization_id: UUID
    trip_no: str
    status: str
    vehicle_id: UUID | None
    trailer_id: UUID | None
    driver_id: UUID | None
    source_ref: str
    expected_buy_amount: str | None
    expected_buy_currency: str | None
    superseded_by: UUID | None


def _as_response(row: Trip) -> TripResponse:
    amount = None if row.expected_buy_amount is None else format(row.expected_buy_amount, "f")
    currency = None if row.expected_buy_currency is None else str(row.expected_buy_currency).strip()
    return TripResponse(
        id=row.id,
        organization_id=row.organization_id,
        trip_no=row.trip_no,
        status=row.status,
        vehicle_id=row.vehicle_id,
        trailer_id=row.trailer_id,
        driver_id=row.driver_id,
        source_ref=row.source_ref,
        expected_buy_amount=amount,
        expected_buy_currency=currency,
        superseded_by=row.superseded_by,
    )


async def _assigned(
    session: AsyncSession,
    resource_id: UUID | None,
    slot: str,
) -> UUID | None:
    if resource_id is None:
        return None
    row = await ResourceService(session).get_resource(resource_id)
    require_trip_slot(slot, row.resource_kind)
    return row.id


@router.get("", response_model=list[TripResponse])
async def list_trips(
    status: str | None = Query(default=None),
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
) -> list[TripResponse]:
    state = None if status is None or status.strip() == "" else status
    rows = await TripService(session).list_trips(status=state)
    return [_as_response(row) for row in rows]


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
async def create_trip(
    body: TripCreate,
    _authz: None = Depends(require_permission(_SHIP, "organization")),
    session: AsyncSession = Depends(require_tenant_session),
    identity: SessionIdentity = Depends(get_current_identity),
) -> TripResponse:
    vehicle_id = await _assigned(session, body.vehicle_id, "vehicle")
    trailer_id = await _assigned(session, body.trailer_id, "trailer")
    driver_id = await _assigned(session, body.driver_id, "driver")
    row = await TripService(session).record_trip(
        organization_id=identity.organization_id,
        user_id=identity.user_id,
        trip_no=body.trip_no,
        status=body.status,
        vehicle_id=vehicle_id,
        trailer_id=trailer_id,
        driver_id=driver_id,
        source_ref=body.source_ref,
        expected_buy_amount=body.expected_buy_amount,
        expected_buy_currency=body.expected_buy_currency,
    )
    await session.commit()
    return _as_response(row)
