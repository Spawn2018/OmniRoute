from uuid import UUID

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai_transforms.extraction.schemas import ExtractionPayload
from app.domain.errors import AcceptRequiresRateLine
from app.domain.rate_line import require_source_ref
from app.models.extraction_draft import ExtractionDraft
from app.models.rate_line import RateLine
from app.services.extraction.extraction_service import ExtractionService
from app.services.rate_lines.rate_line_service import RateLineService


class AcceptExtractionToRates:
    """HITL accept + rate_line w jednym request/transakcji — nie ExtractionService (PROGRAM 1.3)."""

    def __init__(
        self,
        session: AsyncSession,
        extraction: ExtractionService | None = None,
        rates: RateLineService | None = None,
    ) -> None:
        self._extraction = extraction or ExtractionService(session)
        self._rates = rates or RateLineService(session)

    async def accept(
        self,
        *,
        draft_id: UUID,
        user_id: UUID,
    ) -> tuple[ExtractionDraft, list[RateLine]]:
        draft = await self._extraction.accept(draft_id=draft_id, user_id=user_id)
        payload = _require_rate_payload(draft)
        origin = require_source_ref(draft.source_ref)
        written: list[RateLine] = []
        for candidate in payload.candidates:
            written.append(
                await self._rates.create_buy_rate(
                    organization_id=draft.organization_id,
                    user_id=user_id,
                    charge_code=candidate.code,
                    amount=candidate.amount_text,
                    currency=candidate.currency,
                    source_ref=origin,
                ),
            )
        return draft, written


def _require_rate_payload(draft: ExtractionDraft) -> ExtractionPayload:
    try:
        payload = ExtractionPayload.model_validate(draft.payload)
    except ValidationError as exc:
        raise AcceptRequiresRateLine("Szkic nie zawiera poprawnych kandydatów stawki") from exc
    if len(payload.candidates) == 0:
        raise AcceptRequiresRateLine("Akceptacja wymaga kandydata stawki kupna")
    return payload
