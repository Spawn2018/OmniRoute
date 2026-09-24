from datetime import date
from typing import NamedTuple
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.cargo_claim import (
    require_claim_kind,
    require_claim_shipment_id,
    require_claim_source_ref,
    require_cmr_notice_window,
    require_cmr_order,
    require_damage_code,
    require_evidence_gps,
    require_evidence_photo,
    require_evidence_temp,
    require_notice_due_at,
    require_suit_due_at,
)
from app.models.cargo_claim import CargoClaim
from app.repositories.cargo_claims.cargo_claim_repository import CargoClaimRepository


class _NormalizedClaim(NamedTuple):
    shipment_id: UUID
    claim_kind: str
    damage_code: str
    cmr_notice_window: str
    notice_due_at: date
    suit_due_at: date
    evidence_gps: bool
    evidence_temp: bool
    evidence_photo: bool
    source_ref: str


class CargoClaimService:
    def __init__(self, session: AsyncSession) -> None:
        self._claims = CargoClaimRepository(session)

    async def list_claims(self) -> list[CargoClaim]:
        return await self._claims.list_all()

    async def record_claim(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        shipment_id: UUID,
        claim_kind: str,
        damage_code: str,
        cmr_notice_window: str,
        notice_due_at: str,
        suit_due_at: str,
        evidence_gps: bool,
        evidence_temp: bool,
        evidence_photo: bool,
        source_ref: str,
    ) -> CargoClaim:
        draft = self._normalized_create_inputs(
            shipment_id=shipment_id,
            claim_kind=claim_kind,
            damage_code=damage_code,
            cmr_notice_window=cmr_notice_window,
            notice_due_at=notice_due_at,
            suit_due_at=suit_due_at,
            evidence_gps=evidence_gps,
            evidence_temp=evidence_temp,
            evidence_photo=evidence_photo,
            source_ref=source_ref,
        )
        return await self._insert_from_draft(organization_id, user_id, draft)

    def _normalized_create_inputs(
        self,
        *,
        shipment_id: UUID,
        claim_kind: str,
        damage_code: str,
        cmr_notice_window: str,
        notice_due_at: str,
        suit_due_at: str,
        evidence_gps: bool,
        evidence_temp: bool,
        evidence_photo: bool,
        source_ref: str,
    ) -> _NormalizedClaim:
        notice = require_notice_due_at(notice_due_at)
        suit = require_suit_due_at(suit_due_at)
        require_cmr_order(notice, suit)
        return _NormalizedClaim(
            shipment_id=require_claim_shipment_id(shipment_id),
            claim_kind=require_claim_kind(claim_kind),
            damage_code=require_damage_code(damage_code),
            cmr_notice_window=require_cmr_notice_window(cmr_notice_window),
            notice_due_at=notice,
            suit_due_at=suit,
            evidence_gps=require_evidence_gps(evidence_gps),
            evidence_temp=require_evidence_temp(evidence_temp),
            evidence_photo=require_evidence_photo(evidence_photo),
            source_ref=require_claim_source_ref(source_ref),
        )

    async def _insert_from_draft(
        self,
        organization_id: UUID,
        user_id: UUID,
        draft: _NormalizedClaim,
    ) -> CargoClaim:
        row = CargoClaim(
            id=uuid4(),
            organization_id=organization_id,
            shipment_id=draft.shipment_id,
            claim_kind=draft.claim_kind,
            damage_code=draft.damage_code,
            cmr_notice_window=draft.cmr_notice_window,
            notice_due_at=draft.notice_due_at,
            suit_due_at=draft.suit_due_at,
            evidence_gps=draft.evidence_gps,
            evidence_temp=draft.evidence_temp,
            evidence_photo=draft.evidence_photo,
            source_ref=draft.source_ref,
            created_by=user_id,
        )
        return await self._claims.add(row)
