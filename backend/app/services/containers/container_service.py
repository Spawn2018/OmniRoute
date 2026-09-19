from datetime import date, datetime
from decimal import Decimal
from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.container import (
    require_ams_cutoff_at,
    require_booking_no,
    require_cargo_description,
    require_carrier_party_id,
    require_cfs_cutoff_at,
    require_container_bl_kind,
    require_container_delivery_date,
    require_container_gate_in_date,
    require_container_no,
    require_container_pickup_date,
    require_container_quantity,
    require_container_reefer,
    require_container_ref_1,
    require_container_ref_2,
    require_container_ref_3,
    require_container_ref_4,
    require_container_ref_5,
    require_container_remarks,
    require_container_return_date,
    require_container_shipment_id,
    require_container_shipment_leg_id,
    require_container_source_ref,
    require_container_unload_date,
    require_container_volume_m3,
    require_container_weight_kg,
    require_cy_cutoff_at,
    require_demurrage_free_days,
    require_detention_free_days,
    require_free_time_dest_h,
    require_free_time_origin_h,
    require_iso_size_type,
    require_last_survey_at,
    require_mixed_dd_days,
    require_packaging_code,
    require_payload_kg,
    require_pickup_terminal,
    require_pin_code,
    require_return_terminal,
    require_seal_no_1,
    require_seal_no_2,
    require_seal_no_3,
    require_si_cutoff_at,
    require_tare_kg,
    require_teu,
    require_vessel_name,
    require_vgm_cutoff_at,
    require_vgm_kg,
    require_vgm_method,
    require_voyage_no,
)
from app.models.container import Container
from app.repositories.containers.container_repository import ContainerRepository


class _WriteBox(NamedTuple):
    number: object
    size_type: object
    shipment_id: object
    origin: object
    seal: object
    seal2: object
    seal3: object
    vessel: object
    voyage: object
    note: object
    goods: object
    pack: object
    mark: object
    mark2: object
    mark3: object
    mark4: object
    mark5: object
    cold: object
    dock: object
    yard: object
    bill: object
    idle: object
    dwell: object
    demurrage: object
    detention: object
    mixed: object
    cut: object
    ams: object
    cy: object
    cfs: object
    mass: object
    weigh: object
    vgm: object
    survey: object
    book: object
    carrier: object
    leg: object
    tare: object
    pin: object
    payload: object
    teu: object
    qty: object
    kilos: object
    cub: object
    picked: object
    back: object
    gate: object
    deliv: object
    unload: object


class _BoxDraft(NamedTuple):
    number: str
    size_type: str
    shipment_id: UUID | None
    origin: str
    seal: str | None
    seal2: str | None
    seal3: str | None
    vessel: str | None
    voyage: str | None
    note: str | None
    goods: str | None
    pack: str | None
    mark: str | None
    mark2: str | None
    mark3: str | None
    mark4: str | None
    mark5: str | None
    cold: bool
    dock: str | None
    yard: str | None
    bill: str | None
    idle: int | None
    dwell: int | None
    demurrage: int | None
    detention: int | None
    mixed: int | None
    cut: datetime | None
    ams: datetime | None
    cy: datetime | None
    cfs: datetime | None
    mass: Decimal | None
    weigh: str | None
    vgm: datetime | None
    survey: datetime | None
    book: str | None
    carrier: UUID | None
    leg: UUID | None
    tare: Decimal | None
    pin: str | None
    payload: Decimal | None
    teu: Decimal | None
    qty: int | None
    kilos: Decimal | None
    cub: Decimal | None
    picked: date | None
    back: date | None
    gate: date | None
    deliv: date | None
    unload: date | None


def _box_draft(write: _WriteBox) -> _BoxDraft:
    clocks = _require_clocks(write)
    return _BoxDraft(
        require_container_no(write.number),
        require_iso_size_type(write.size_type),
        require_container_shipment_id(write.shipment_id),
        require_container_source_ref(write.origin),
        require_seal_no_1(write.seal),
        require_seal_no_2(write.seal2),
        require_seal_no_3(write.seal3),
        require_vessel_name(write.vessel),
        require_voyage_no(write.voyage),
        require_container_remarks(write.note),
        require_cargo_description(write.goods),
        require_packaging_code(write.pack),
        require_container_ref_1(write.mark),
        require_container_ref_2(write.mark2),
        require_container_ref_3(write.mark3),
        require_container_ref_4(write.mark4),
        require_container_ref_5(write.mark5),
        require_container_reefer(write.cold),
        require_pickup_terminal(write.dock),
        require_return_terminal(write.yard),
        require_container_bl_kind(write.bill),
        *clocks,
        require_vgm_kg(write.mass),
        require_vgm_method(write.weigh),
        require_vgm_cutoff_at(write.vgm),
        require_last_survey_at(write.survey),
        require_booking_no(write.book),
        require_carrier_party_id(write.carrier),
        require_container_shipment_leg_id(write.leg),
        require_tare_kg(write.tare),
        require_pin_code(write.pin), require_payload_kg(write.payload),
        require_teu(write.teu), require_container_quantity(write.qty),
        require_container_weight_kg(write.kilos), require_container_volume_m3(write.cub),
        require_container_pickup_date(write.picked), require_container_return_date(write.back),
        require_container_gate_in_date(write.gate), require_container_delivery_date(write.deliv),
        require_container_unload_date(write.unload),
    )


def _require_clocks(write: _WriteBox) -> tuple[
    int | None, int | None, int | None, int | None, int | None,
    datetime | None, datetime | None, datetime | None, datetime | None,
]:
    return (
        require_free_time_origin_h(write.idle),
        require_free_time_dest_h(write.dwell),
        require_demurrage_free_days(write.demurrage),
        require_detention_free_days(write.detention),
        require_mixed_dd_days(write.mixed),
        require_si_cutoff_at(write.cut),
        require_ams_cutoff_at(write.ams),
        require_cy_cutoff_at(write.cy),
        require_cfs_cutoff_at(write.cfs),
    )


def _box_unchanged(current: Container, draft: _BoxDraft) -> bool:
    return (
        current.iso_size_type == draft.size_type
        and current.shipment_id == draft.shipment_id
        and current.source_ref == draft.origin
        and current.seal_no_1 == draft.seal
        and current.seal_no_2 == draft.seal2
        and current.seal_no_3 == draft.seal3
        and current.vessel_name == draft.vessel
        and current.voyage_no == draft.voyage
        and current.remarks == draft.note
        and current.cargo_description == draft.goods
        and current.packaging_code == draft.pack
        and current.ref_1 == draft.mark
        and current.ref_2 == draft.mark2
        and current.ref_3 == draft.mark3
        and current.ref_4 == draft.mark4
        and current.ref_5 == draft.mark5
        and current.reefer == draft.cold
        and current.pickup_terminal == draft.dock
        and current.return_terminal == draft.yard
        and current.bl_kind == draft.bill
        and _clocks_match(current, draft)
        and current.vgm_kg == draft.mass
        and current.vgm_method == draft.weigh
        and current.vgm_cutoff_at == draft.vgm
        and current.last_survey_at == draft.survey
        and current.booking_no == draft.book
        and current.carrier_party_id == draft.carrier
        and current.shipment_leg_id == draft.leg
        and current.tare_kg == draft.tare
        and current.pin_code == draft.pin
        and current.payload_kg == draft.payload
        and current.teu == draft.teu
        and current.quantity == draft.qty
        and current.weight_kg == draft.kilos and current.volume_m3 == draft.cub
        and current.pickup_date == draft.picked and current.return_date == draft.back
        and current.gate_in_date == draft.gate and current.delivery_date == draft.deliv
        and current.unload_date == draft.unload
    )


def _clocks_match(current: Container, draft: _BoxDraft) -> bool:
    return (
        current.free_time_origin_h == draft.idle
        and current.free_time_dest_h == draft.dwell
        and current.demurrage_free_days == draft.demurrage
        and current.detention_free_days == draft.detention
        and current.mixed_dd_days == draft.mixed
        and current.si_cutoff_at == draft.cut
        and current.ams_cutoff_at == draft.ams
        and current.cy_cutoff_at == draft.cy
        and current.cfs_cutoff_at == draft.cfs
    )


def _container_row(organization_id: UUID, user_id: UUID, draft: _BoxDraft) -> Container:
    return Container(
        id=uuid4(),
        organization_id=organization_id,
        container_no=draft.number,
        iso_size_type=draft.size_type,
        shipment_id=draft.shipment_id,
        source_ref=draft.origin,
        seal_no_1=draft.seal, seal_no_2=draft.seal2, seal_no_3=draft.seal3,
        vessel_name=draft.vessel, voyage_no=draft.voyage, remarks=draft.note,
        cargo_description=draft.goods, packaging_code=draft.pack,
        ref_1=draft.mark, ref_2=draft.mark2, ref_3=draft.mark3,
        ref_4=draft.mark4, ref_5=draft.mark5, reefer=draft.cold,
        pickup_terminal=draft.dock, return_terminal=draft.yard, bl_kind=draft.bill,
        **_clock_kwargs(draft),
        vgm_kg=draft.mass, vgm_method=draft.weigh, vgm_cutoff_at=draft.vgm,
        last_survey_at=draft.survey, booking_no=draft.book,
        carrier_party_id=draft.carrier, shipment_leg_id=draft.leg,
        tare_kg=draft.tare, pin_code=draft.pin, payload_kg=draft.payload, teu=draft.teu,
        quantity=draft.qty, weight_kg=draft.kilos, volume_m3=draft.cub,
        pickup_date=draft.picked, return_date=draft.back, gate_in_date=draft.gate,
        delivery_date=draft.deliv, unload_date=draft.unload, created_by=user_id,
    )


def _clock_kwargs(draft: _BoxDraft) -> dict[str, object]:
    return {
        "free_time_origin_h": draft.idle,
        "free_time_dest_h": draft.dwell,
        "demurrage_free_days": draft.demurrage,
        "detention_free_days": draft.detention,
        "mixed_dd_days": draft.mixed,
        "si_cutoff_at": draft.cut,
        "ams_cutoff_at": draft.ams,
        "cy_cutoff_at": draft.cy,
        "cfs_cutoff_at": draft.cfs,
    }


class ContainerService:
    def __init__(self, session: AsyncSession) -> None:
        self._rows = ContainerRepository(session)

    async def list_containers(self, *, iso_size_type: object | None = None) -> list[Container]:
        size_type = None if iso_size_type is None else require_iso_size_type(iso_size_type)
        return await self._rows.list_current(size_type)

    async def _persist_box(
        self,
        organization_id: UUID,
        user_id: UUID,
        draft: _BoxDraft,
    ) -> Container:
        current = await self._rows.find_current(draft.number)
        if current is not None and _box_unchanged(current, draft):
            return current
        saved = await self._rows.add(_container_row(organization_id, user_id, draft))
        if current is not None:
            await self._rows.mark_superseded(current, saved.id)
        return saved

    async def record_container(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        write: _WriteBox,
    ) -> Container:
        return await self._persist_box(organization_id, user_id, _box_draft(write))
