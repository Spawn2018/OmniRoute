from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.stop import (
    require_eta_legal,
    require_eta_physical,
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


@dataclass(frozen=True)
class _PackedPoint:
    order_id: UUID
    place_id: UUID
    kind: str
    seq: int
    zone: str
    state: str
    origin: str
    physical: datetime
    legal: datetime


def _pack_point(
    *,
    shipment_id: object,
    location_id: object,
    stop_kind: object,
    sequence_no: object,
    time_zone: object,
    status: object,
    source_ref: object,
    eta_physical: object,
    eta_legal: object,
) -> _PackedPoint:
    return _PackedPoint(
        order_id=require_stop_shipment_id(shipment_id),
        place_id=require_stop_location_id(location_id),
        kind=require_stop_kind(stop_kind),
        seq=require_sequence_no(sequence_no),
        zone=require_time_zone(time_zone),
        state=require_stop_status(status),
        origin=require_stop_source_ref(source_ref),
        physical=require_eta_physical(eta_physical),
        legal=require_eta_legal(eta_legal),
    )


def _same_point(current: Stop, packed: _PackedPoint) -> bool:
    return (
        current.location_id == packed.place_id
        and current.stop_kind == packed.kind
        and current.time_zone == packed.zone
        and current.status == packed.state
        and current.source_ref == packed.origin
        and current.eta_physical == packed.physical
        and current.eta_legal == packed.legal
    )


class StopService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = StopRepository(session)

    async def get_stop(self, stop_id: UUID) -> Stop:
        found = await self._rows.get(stop_id)
        if found is None:
            raise ResourceNotFound("nieznany punkt operacyjny")
        return found

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
        eta_physical: object,
        eta_legal: object,
    ) -> Stop:
        packed = _pack_point(
            shipment_id=shipment_id,
            location_id=location_id,
            stop_kind=stop_kind,
            sequence_no=sequence_no,
            time_zone=time_zone,
            status=status,
            source_ref=source_ref,
            eta_physical=eta_physical,
            eta_legal=eta_legal,
        )
        current = await self._rows.find_current(packed.order_id, packed.seq)
        if current is not None and _same_point(current, packed):
            return current
        saved = await self._insert(organization_id, user_id, packed)
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

    async def _insert(self, organization_id: UUID, user_id: UUID, packed: _PackedPoint) -> Stop:
        return await self._rows.add(
            Stop(
                id=uuid4(),
                organization_id=organization_id,
                shipment_id=packed.order_id,
                location_id=packed.place_id,
                stop_kind=packed.kind,
                sequence_no=packed.seq,
                time_zone=packed.zone,
                status=packed.state,
                source_ref=packed.origin,
                eta_physical=packed.physical,
                eta_legal=packed.legal,
                created_by=user_id,
            ),
        )
