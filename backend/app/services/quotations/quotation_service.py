from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.charge_code import normalize_charge_code
from app.domain.errors import (
    DomainError,
    IncompleteQuotationSnapshot,
    InvalidCustomerRfq,
    InvalidQuotationDocumentNumber,
    QuotationGap,
    ResourceNotFound,
    UnknownChargeCode,
    UnknownCommodityCode,
    UnknownDangerousGood,
    UnknownParty,
    UnknownPort,
)
from app.domain.quotation import (
    require_batch_charge_codes,
    require_document_number_prefix,
    require_lane_party_snapshot,
    require_quotation_incoterm,
    require_valid_until,
)
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
    if "fk_quotation_customer_rfq" in detail:
        return InvalidCustomerRfq("nieznane zapytanie ofertowe wyceny")
    if "fk_quotation_commodity_code" in detail:
        return UnknownCommodityCode("nieznany kod towarowy wyceny")
    if "fk_quotation_dangerous_good" in detail:
        return UnknownDangerousGood("nieznany towar niebezpieczny wyceny")
    if "uq_quotation_org_document_number" in detail:
        return InvalidQuotationDocumentNumber("numer oferty już zajęty")
    if "ck_quotation_incoterm" in detail:
        return IncompleteQuotationSnapshot("incoterm wyceny poza allowlistą")
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
        customer_rfq_id: UUID | None = None,
    ) -> list[Quotation]:
        return await self._quotations.list_all(
            party_id=party_id,
            origin_port_id=origin_port_id,
            destination_port_id=destination_port_id,
            customer_rfq_id=customer_rfq_id,
        )

    async def get_quotation(self, quotation_id: UUID) -> Quotation:
        found = await self._quotations.get(quotation_id)
        if found is None:
            raise ResourceNotFound("nieznana wycena")
        return found

    async def quote_from_current_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        origin_port_id: UUID | None,
        destination_port_id: UUID | None,
        party_id: UUID | None,
        customer_rfq_id: UUID | None = None,
        commodity_code_id: UUID | None = None,
        dangerous_good_id: UUID | None = None,
        incoterm: object = None,
        incoterms_version: object = None,
        trade_side: object = None,
        named_place: object = None,
        valid_until: object = None,
    ) -> Quotation:
        catalog = await self._require_catalog(charge_code)
        origin, destination, party = require_lane_party_snapshot(
            origin_port_id, destination_port_id, party_id,
        )
        terms = require_quotation_incoterm(
            incoterm, incoterms_version, trade_side, named_place,
        )
        until = require_valid_until(valid_until)
        return await self._insert_from_rate(
            organization_id=organization_id,
            user_id=user_id,
            charge_code=catalog.code,
            origin_port_id=origin,
            destination_port_id=destination,
            party_id=party,
            customer_rfq_id=customer_rfq_id,
            commodity_code_id=commodity_code_id,
            dangerous_good_id=dangerous_good_id,
            terms=terms,
            valid_until=until,
        )

    async def quote_batch_from_current_rates(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_codes: list[str],
        origin_port_id: UUID | None,
        destination_port_id: UUID | None,
        party_id: UUID | None,
        customer_rfq_id: UUID | None = None,
        commodity_code_id: UUID | None = None,
        dangerous_good_id: UUID | None = None,
        incoterm: object = None,
        incoterms_version: object = None,
        trade_side: object = None,
        named_place: object = None,
        valid_until: object = None,
    ) -> list[Quotation]:
        codes = require_batch_charge_codes(charge_codes)
        quoted: list[Quotation] = []
        for code in codes:
            quoted.append(
                await self.quote_from_current_rate(
                    organization_id=organization_id,
                    user_id=user_id,
                    charge_code=code,
                    origin_port_id=origin_port_id,
                    destination_port_id=destination_port_id,
                    party_id=party_id,
                    customer_rfq_id=customer_rfq_id,
                    commodity_code_id=commodity_code_id,
                    dangerous_good_id=dangerous_good_id,
                    incoterm=incoterm,
                    incoterms_version=incoterms_version,
                    trade_side=trade_side,
                    named_place=named_place,
                    valid_until=valid_until,
                )
            )
        return quoted

    async def _insert_from_rate(
        self,
        *,
        organization_id: UUID,
        user_id: UUID,
        charge_code: str,
        origin_port_id: UUID,
        destination_port_id: UUID,
        party_id: UUID,
        customer_rfq_id: UUID | None,
        commodity_code_id: UUID | None,
        dangerous_good_id: UUID | None,
        terms: tuple[str | None, str | None, str | None, str | None],
        valid_until: object,
    ) -> Quotation:
        try:
            quoted = await self._quotations.insert_from_current_rate(
                organization_id=organization_id,
                created_by=user_id,
                charge_code=charge_code,
                origin_port_id=origin_port_id,
                destination_port_id=destination_port_id,
                party_id=party_id,
                customer_rfq_id=customer_rfq_id,
                commodity_code_id=commodity_code_id,
                dangerous_good_id=dangerous_good_id,
                incoterm=terms[0],
                incoterms_version=terms[1],
                trade_side=terms[2],
                named_place=terms[3],
                valid_until=valid_until,
            )
        except IntegrityError as exc:
            mapped = _snapshot_integrity_error(exc)
            if mapped is None:
                raise
            raise mapped from exc
        if quoted is None:
            raise QuotationGap(f"quotation_gap: brak bieżącej stawki dla {charge_code}")
        return quoted

    async def set_valid_until(
        self,
        quotation_id: UUID,
        valid_until: object,
    ) -> Quotation:
        row = await self._quotations.get(quotation_id)
        if row is None:
            raise ResourceNotFound("nieznana wycena")
        row.valid_until = require_valid_until(valid_until)
        return await self._quotations.save(row)

    async def set_noted_credit_review(
        self,
        quotation_id: UUID,
        credit_review_id: UUID,
    ) -> Quotation:
        row = await self._quotations.get(quotation_id)
        if row is None:
            raise ResourceNotFound("nieznana wycena")
        row.noted_credit_review_id = credit_review_id
        return await self._quotations.save(row)

    async def set_negotiated_channel_quote(
        self,
        quotation_id: UUID,
        channel_quote_id: UUID,
    ) -> Quotation:
        row = await self._quotations.get(quotation_id)
        if row is None:
            raise ResourceNotFound("nieznana wycena")
        row.negotiated_channel_quote_id = channel_quote_id
        return await self._quotations.save(row)

    async def issue_document_number(
        self,
        *,
        quotation_id: UUID,
        prefix: str | None,
    ) -> Quotation:
        token = require_document_number_prefix(prefix)
        current = await self._quotations.get(quotation_id)
        if current is None:
            raise ResourceNotFound("nieznana wycena")
        if current.document_number is not None:
            return current
        return await self._assign_document_number(quotation_id, token)

    async def _assign_document_number(self, quotation_id: UUID, prefix: str) -> Quotation:
        try:
            issued = await self._quotations.issue_document_number(
                quotation_id=quotation_id,
                prefix=prefix,
            )
        except IntegrityError as exc:
            mapped = _snapshot_integrity_error(exc)
            if mapped is not None:
                raise mapped from exc
            return await self._reload_issued(quotation_id)
        if issued is None:
            return await self._reload_issued(quotation_id)
        return issued

    async def _reload_issued(self, quotation_id: UUID) -> Quotation:
        again = await self._quotations.get(quotation_id)
        if again is None:
            raise ResourceNotFound("nieznana wycena")
        if again.document_number is not None:
            return again
        raise InvalidQuotationDocumentNumber("nie udało się nadać numeru oferty")

    async def _require_catalog(self, charge_code: str) -> ChargeCode:
        token = normalize_charge_code(charge_code)
        catalog = await self._codes.find_by_token(token)
        if catalog is None:
            raise UnknownChargeCode(f"nieznany kod opłaty: {token}")
        return catalog
