from typing import NamedTuple
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_transforms.extraction.schemas import ExtractedChargeCandidate, ExtractionPayload
from app.domain.errors import AcceptRequiresRateLine, InvalidExtractionDraft
from app.domain.extraction_draft import (
    extraction_carrier_quote_kind,
    extraction_rate_kind,
    extraction_tender_rfp_kind,
    require_bulk_accept_confidence,
    require_candidate_indexes,
    require_carrier_quote_payload,
    require_extraction_draft_kind,
    require_tender_rfp_payload,
    split_candidates_by_indexes,
)
from app.domain.rate_line import require_source_ref
from app.models.channel_quote import ChannelQuote
from app.models.extraction_draft import ExtractionDraft
from app.models.rate_line import RateLine
from app.services.channel_quotes.channel_quote_service import ChannelQuoteService
from app.services.extraction.extraction_service import ExtractionService
from app.services.rate_lines.rate_line_service import RateLineService
from app.services.tender_rfp_intakes.tender_rfp_intake_service import TenderRfpIntakeService
from app.services.tenders.tender_service import TenderService


class ExtractionAcceptResult(NamedTuple):
    draft: ExtractionDraft
    rate_lines: list[RateLine]
    channel_quotes: list[ChannelQuote]


class AcceptExtractionToRates:
    """HITL accept + zapis w API — nie ExtractionService (PROGRAM 1.3 / O6)."""

    def __init__(
        self,
        session: AsyncSession,
        extraction: ExtractionService | None = None,
        rates: RateLineService | None = None,
        quotes: ChannelQuoteService | None = None,
        intakes: TenderRfpIntakeService | None = None,
        boards: TenderService | None = None,
    ) -> None:
        self._extraction = extraction or ExtractionService(session)
        self._rates = rates or RateLineService(session)
        self._quotes = quotes or ChannelQuoteService(session)
        self._intakes = intakes or TenderRfpIntakeService(session)
        self._boards = boards or TenderService(session)

    async def accept(
        self,
        *,
        draft_id: UUID,
        user_id: UUID,
        candidate_indexes: list[int] | None = None,
    ) -> ExtractionAcceptResult:
        pending = await self._extraction.require_pending(draft_id)
        kind = require_extraction_draft_kind(getattr(pending, "draft_kind", None))
        if kind == extraction_rate_kind():
            return await self._accept_rates(
                pending,
                user_id,
                candidate_indexes=candidate_indexes,
            )
        if candidate_indexes is not None:
            raise InvalidExtractionDraft("partial accept tylko dla rate_line")
        draft = await self._extraction.accept(draft_id=draft_id, user_id=user_id)
        if kind == extraction_tender_rfp_kind():
            await self._write_intake(draft, user_id)
            return ExtractionAcceptResult(draft, [], [])
        if kind == extraction_carrier_quote_kind():
            quote = await self._write_channel_quote(draft, user_id)
            return ExtractionAcceptResult(draft, [], [quote])
        raise AcceptRequiresRateLine("Szkic nie jest rate_line")

    async def _accept_rates(
        self,
        draft: ExtractionDraft,
        user_id: UUID,
        *,
        candidate_indexes: list[int] | None,
    ) -> ExtractionAcceptResult:
        payload = _require_rate_payload(draft)
        indexes = require_candidate_indexes(candidate_indexes, len(payload.candidates))
        selected, remaining = split_candidates_by_indexes(payload.candidates, indexes)
        require_bulk_accept_confidence(selected)
        origin = require_source_ref(draft.source_ref)
        written: list[RateLine] = []
        for candidate in selected:
            row = _as_charge_candidate(candidate)
            written.append(
                await self._rates.create_buy_rate(
                    organization_id=draft.organization_id,
                    user_id=user_id,
                    charge_code=row.code,
                    amount=row.amount_text,
                    currency=row.currency,
                    source_ref=origin,
                ),
            )
        leftover = [_as_charge_candidate(row).model_dump() for row in remaining]
        updated = await self._extraction.apply_rate_accept_result(
            draft_id=draft.id,
            user_id=user_id,
            remaining_candidates=leftover,
            mark_accepted=len(leftover) == 0,
        )
        return ExtractionAcceptResult(updated, written, [])

    async def _write_channel_quote(self, draft: ExtractionDraft, user_id: UUID) -> ChannelQuote:
        stored = require_carrier_quote_payload(draft.payload)
        return await self._quotes.create_quote(
            organization_id=draft.organization_id,
            user_id=user_id,
            party_id=stored.party_id,
            origin_port_id=stored.origin_port_id,
            destination_port_id=stored.destination_port_id,
            quote_date=stored.quote_date,
            amount=stored.amount,
            currency=stored.currency,
            transit_days=stored.transit_days,
            source_ref=draft.source_ref,
        )

    async def _write_intake(self, draft: ExtractionDraft, user_id: UUID) -> None:
        stored = require_tender_rfp_payload(draft.payload)
        board = await self._boards.get_board(stored.tender_id)
        await self._intakes.persist_intake(
            organization_id=draft.organization_id,
            user_id=user_id,
            tender_id=board.id,
            intake_code=stored.intake_code,
            source_ref=f"fixture://tender-rfp-intake/{draft.id}",
        )


def _as_charge_candidate(raw: object) -> ExtractedChargeCandidate:
    if isinstance(raw, ExtractedChargeCandidate):
        return raw
    return ExtractedChargeCandidate.model_validate(raw)


def _require_rate_payload(draft: ExtractionDraft) -> ExtractionPayload:
    try:
        payload = ExtractionPayload.model_validate(draft.payload)
    except ValidationError as exc:
        raise AcceptRequiresRateLine("Szkic nie zawiera poprawnych kandydatów stawki") from exc
    if not payload.candidates:
        raise AcceptRequiresRateLine("Szkic nie zawiera kandydatów stawki")
    return payload
