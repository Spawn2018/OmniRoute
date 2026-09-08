from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.stop import (
    require_sequence_no,
    require_stop_kind,
    require_stop_location_id,
    require_stop_shipment_id,
    require_stop_source_ref,
    require_stop_status,
    require_time_zone,
)
from app.models.stop import Stop
from app.repositories.stops.stop_repository import StopRepository


def _same_point(
    current: Stop,
    *,
    place_id: UUID,
    kind: str,
    zone: str,
    state: str,
    origin: str,
) -> bool:
    return (
        current.location_id == place_id
        and current.stop_kind == kind
        and current.time_zone == zone
        and current.status == state
        and current.source_ref == origin
    )


class StopService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = StopRepository(session)

    async def list_for_shipment(self, shipment_id: object) -> list[Stop]:
        return await self._rows.list_current_for_shipment(require_stop_shipment_id(shipment_id))

    async def record_stop(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: object,
        location_id: object,
        stop_kind: object,
        sequence_no: object,
        time_zone: object,
        status: object,
        source_ref: object,
    ) -> Stop:
        order_id = require_stop_shipment_id(shipment_id)
        place_id = require_stop_location_id(location_id)
        kind = require_stop_kind(stop_kind)
        seq = require_sequence_no(sequence_no)
        zone = require_time_zone(time_zone)
        state = require_stop_status(status)
        origin = require_stop_source_ref(source_ref)
        current = await self._rows.find_current(order_id, seq)
        if current is not None and _same_point(
            current, place_id=place_id, kind=kind, zone=zone, state=state, origin=origin
        ):
            return current
        saved = await self._insert(
            organization_id=organization_id,
            user_id=user_id,
            order_id=order_id,
            place_id=place_id,
            kind=kind,
            seq=seq,
            zone=zone,
            state=state,
            origin=origin,
        )
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

    async def _insert(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        order_id: UUID,
        place_id: UUID,
        kind: str,
        seq: int,
        zone: str,
        state: str,
        origin: str,
    ) -> Stop:
        return await self._rows.add(
            Stop(
                id=uuid4(),
                organization_id=organization_id,
                shipment_id=order_id,
                location_id=place_id,
                stop_kind=kind,
                sequence_no=seq,
                time_zone=zone,
                status=state,
                source_ref=origin,
                created_by=user_id,
            ),
        )
