from dataclasses import dataclass
from typing import NoReturn
from uuid import UUID, uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.errors import InvalidShipment, ResourceNotFound, ShipmentConflict
from app.domain.shipment import (
    require_guide_code,
    require_is_waste,
    require_optional_label,
    require_parent_pair,
    require_parent_shipment_id,
    require_party_on_quotation,
    require_quotation_id,
    require_relation_kind,
    require_shipment_anchor_date,
    require_shipment_ref,
    require_shipment_source_ref,
    shipment_draft_status,
)
from app.models.shipment import Shipment
from app.repositories.shipments.shipment_repository import ShipmentRepository


@dataclass(frozen=True, slots=True)
class ShipmentHitlFields:
    shipment_ref: object = None
    parent_shipment_id: object = None
    relation_kind: object = None
    guide_code: object = None
    plant_label: object = None
    carrier_label: object = None
    asn_id: UUID | None = None
    is_waste: object = None
    etd: object = None
    loading_date: object = None
    unloading_date: object = None
    invoice_date: object = None


def _raise_create_conflict(orig: IntegrityError) -> NoReturn:
    detail = str(orig.orig) if orig.orig is not None else str(orig)
    if "uq_shipment_org_quotation" in detail:
        raise ShipmentConflict("to zlecenie już istnieje dla tej wyceny") from orig
    if "uq_shipment_org_shipment_ref" in detail:
        raise ShipmentConflict("ten numer zlecenia już istnieje") from orig
    if "uq_shipment_org_asn" in detail:
        raise ShipmentConflict("to awizo już ma zlecenie") from orig
    if "fk_shipment_asn" in detail:
        raise InvalidShipment("awizo nie istnieje") from orig
    if "fk_shipment_parent" in detail:
        raise InvalidShipment("główne zlecenie nie istnieje") from orig
    raise orig


def _draft_shipment(
    *,
    row_id: UUID,
    organization_id: UUID,
    user_id: UUID,
    quotation_id: UUID,
    party_id: UUID,
    source_ref: str,
    hitl: ShipmentHitlFields,
) -> Shipment:
    parent = require_parent_shipment_id(hitl.parent_shipment_id)
    kind = require_relation_kind(hitl.relation_kind)
    require_parent_pair(parent, kind, child_id=row_id)
    return Shipment(
        id=row_id,
        organization_id=organization_id,
        quotation_id=require_quotation_id(quotation_id),
        party_id=require_party_on_quotation(party_id),
        source_ref=require_shipment_source_ref(source_ref),
        shipment_ref=require_shipment_ref(hitl.shipment_ref),
        parent_shipment_id=parent,
        relation_kind=kind,
        guide_code=require_guide_code(hitl.guide_code),
        plant_label=require_optional_label(hitl.plant_label, "zakład"),
        carrier_label=require_optional_label(hitl.carrier_label, "przewoźnik"),
        asn_id=hitl.asn_id,
        is_waste=require_is_waste(hitl.is_waste),
        etd=require_shipment_anchor_date(hitl.etd),
        loading_date=require_shipment_anchor_date(hitl.loading_date),
        unloading_date=require_shipment_anchor_date(hitl.unloading_date),
        invoice_date=require_shipment_anchor_date(hitl.invoice_date),
        status=shipment_draft_status(),
        created_by=user_id,
    )


class ShipmentService:
    def __init__(self, session: AsyncSession) -> None:
        self._shipments = ShipmentRepository(session)

    async def list_shipments(self) -> list[Shipment]:
        return await self._shipments.list_all()

    async def get_shipment(self, shipment_id: UUID) -> Shipment:
        found = await self._shipments.get(shipment_id)
        if found is None:
            raise ResourceNotFound("nieznane zlecenie")
        return found

    async def create_shipment(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        quotation_id: UUID,
        party_id: UUID,
        source_ref: str,
        hitl: ShipmentHitlFields | None = None,
    ) -> Shipment:
        row = _draft_shipment(
            row_id=uuid4(),
            organization_id=organization_id,
            user_id=user_id,
            quotation_id=quotation_id,
            party_id=party_id,
            source_ref=source_ref,
            hitl=hitl or ShipmentHitlFields(),
        )
        try:
            return await self._shipments.add(row)
        except IntegrityError as orig:
            _raise_create_conflict(orig)
