from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import (
    DomainError,
    IncompleteQuotationSnapshot,
    QuotationGap,
    UnknownChargeCode,
    UnknownParty,
    UnknownPort,
)
from app.domain.quotation import require_lane_party_snapshot
from app.models.charge_code import ChargeCode
from app.models.quotation import Quotation
from app.repositories.charge_codes.charge_code_repository import ChargeCodeRepository
from app.repositories.quotations.quotation_repository import QuotationRepository


def _snapshot_integrity_error(exc: IntegrityError) -> DomainError | None:
    detail = str(exc.orig) if exc.orig is not None else str(exc)
    if "fk_quotation_party" in detail:
        return UnknownParty("nieznany kontrahent wyceny")
    if "fk_quotation_origin_port" in detail or "fk_quotation_destination_port" in detail:
        return UnknownPort("nieznany port wyceny")
    if "ck_quotation_lane_party_complete" in detail:
        return IncompleteQuotationSnapshot("wycena wymaga POL, POD i kontrahenta")
    return None


class QuotationService:
    def __init__(self, session: AsyncSession) -> None:
        self._quotations = QuotationRepository(session)
        self._codes = ChargeCodeRepository(session)

    async def list_quotations(
        self,
        *,
        party_id: UUID | None = None,
        origin_port_id: UUID | None = None,
        destination_port_id: UUID | None = None,
    ) -> list[Quotation]:
        return await self._quotations.list_all(
            party_id=party_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
        )

    async def quote_from_current_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        origin_port_id: UUID | None,
        destination_port_id: UUID | None,
        party_id: UUID | None,
    ) -> Quotation:
        catalog = await self._require_catalog(charge_code)
        origin, destination, party = require_lane_party_snapshot(
            origin_port_id,
            destination_port_id,
            party_id,
        )
        try:
            quoted = await self._quotations.insert_from_current_rate(
                organization_id=organization_id,
                created_by=user_id,
                charge_code=catalog.code,
                origin_port_id=origin,
                destination_port_id=destination,
                party_id=party,
            )
        except IntegrityError as exc:
            mapped = _snapshot_integrity_error(exc)
            if mapped is None:
                raise
            raise mapped from exc
        if quoted is None:
            raise QuotationGap(f"quotation_gap: brak bieżącej stawki dla {catalog.code}")
        return quoted

    async def _require_catalog(self, charge_code: str) -> ChargeCode:
        token = normalize_charge_code(charge_code)
        catalog = await self._codes.find_by_token(token)
        if catalog is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return catalog
