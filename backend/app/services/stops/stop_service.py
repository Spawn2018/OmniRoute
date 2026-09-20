from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import ResourceNotFound
from app.domain.stop import (
    require_eta_legal,
    require_eta_physical,
    require_notes_for_driver,
    require_sequence_no,
    require_stop_appointment_ref,
    require_stop_group_code,
    require_stop_group_id,
    require_stop_kind,
    require_stop_location_id,
    require_stop_packaging_code,
    require_stop_pod_quality,
    require_stop_quantity,
    require_stop_seal_in,
    require_stop_seal_out,
    require_stop_shipment_id,
    require_stop_source_ref,
    require_stop_status,
    require_stop_waiting_free_minutes,
    require_stop_waiting_started_at,
    require_stop_weight_kg,
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
    group_code: str | None
    group_id: UUID | None
    driver_notes: str | None
    mass: Decimal | None
    count: int | None
    pack: str | None
    inbound_seal: str | None
    outbound_seal: str | None
    appointment: str | None
    wait_free: int | None
    wait_start: datetime | None
    pod: str | None
    physical: datetime
    legal: datetime


@dataclass(frozen=True)
class _HitlTail:
    group_code: object = None
    group_id: object = None
    driver_notes: object = None
    mass: object = None
    count: object = None
    pack: object = None
    inbound_seal: object = None
    outbound_seal: object = None
    appointment: object = None
    wait_free: object = None
    wait_start: object = None
    pod: object = None


def _optional_group_id(raw: object) -> UUID | None:
    if raw is None:
        return None
    return require_stop_group_id(raw)


def _pack_point(
    shipment_id: object,
    location_id: object,
    stop_kind: object,
    sequence_no: object,
    time_zone: object,
    status: object,
    source_ref: object,
    eta_physical: object,
    eta_legal: object,
    tail: _HitlTail,
) -> _PackedPoint:
    return _PackedPoint(
        order_id=require_stop_shipment_id(shipment_id),
        place_id=require_stop_location_id(location_id),
        kind=require_stop_kind(stop_kind),
        seq=require_sequence_no(sequence_no),
        zone=require_time_zone(time_zone),
        state=require_stop_status(status),
        origin=require_stop_source_ref(source_ref),
        group_code=require_stop_group_code(tail.group_code),
        group_id=_optional_group_id(tail.group_id),
        driver_notes=require_notes_for_driver(tail.driver_notes),
        mass=require_stop_weight_kg(tail.mass),
        count=require_stop_quantity(tail.count),
        pack=require_stop_packaging_code(tail.pack),
        inbound_seal=require_stop_seal_in(tail.inbound_seal),
        outbound_seal=require_stop_seal_out(tail.outbound_seal),
        appointment=require_stop_appointment_ref(tail.appointment),
        wait_free=require_stop_waiting_free_minutes(tail.wait_free),
        wait_start=require_stop_waiting_started_at(tail.wait_start),
        pod=require_stop_pod_quality(tail.pod),
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
        and current.stop_group_code == packed.group_code
        and current.stop_group_id == packed.group_id
        and current.notes_for_driver == packed.driver_notes
        and current.weight_kg == packed.mass
        and current.quantity == packed.count
        and current.packaging_code == packed.pack
        and current.seal_in == packed.inbound_seal
        and current.seal_out == packed.outbound_seal
        and current.appointment_ref == packed.appointment
        and current.waiting_free_minutes == packed.wait_free
        and current.waiting_started_at == packed.wait_start
        and current.pod_quality == packed.pod
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
        stop_group_code: object = None,
        stop_group_id: object = None,
        notes_for_driver: object = None,
        weight_kg: object = None,
        quantity: object = None,
        packaging_code: object = None,
        seal_in: object = None,
        seal_out: object = None,
        appointment_ref: object = None,
        waiting_free_minutes: object = None,
        waiting_started_at: object = None,
        pod_quality: object = None,
    ) -> Stop:
        tail = _HitlTail(
            stop_group_code, stop_group_id, notes_for_driver, weight_kg, quantity,
            packaging_code, seal_in, seal_out, appointment_ref, waiting_free_minutes,
            waiting_started_at, pod_quality,
        )
        packed = _pack_point(
            shipment_id, location_id, stop_kind, sequence_no, time_zone, status, source_ref,
            eta_physical, eta_legal, tail)
        return await self._persist(organization_id, user_id, packed)

    async def _persist(
        self,
        organization_id: UUID,
        user_id: UUID,
        packed: _PackedPoint,
    ) -> Stop:
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
                stop_group_code=packed.group_code,
                stop_group_id=packed.group_id,
                notes_for_driver=packed.driver_notes,
                weight_kg=packed.mass,
                quantity=packed.count,
                packaging_code=packed.pack,
                seal_in=packed.inbound_seal,
                seal_out=packed.outbound_seal,
                appointment_ref=packed.appointment,
                waiting_free_minutes=packed.wait_free,
                waiting_started_at=packed.wait_start,
                pod_quality=packed.pod,
                eta_physical=packed.physical,
                eta_legal=packed.legal,
                created_by=user_id,
            ),
        )
