"""Deterministyczny ekstraktor — bez płatnego LLM w CI (plaster 0.7)."""

import re

from app.ai_transforms.extraction.schemas import ExtractedChargeCandidate, ExtractionPayload

_LINE_RE = re.compile(
    r"(?P<code>[A-Z]{2,8})\s+(?P<amount>\d+(?:[.,]\d{1,4})?)\s+(?P<currency>[A-Z]{3})",
)


class MockExtractor:
    def extract(self, *, source_ref: str, input_text: str) -> ExtractionPayload:
        candidates: list[ExtractedChargeCandidate] = []
        consumed: list[str] = []
        for match in _LINE_RE.finditer(input_text):
            candidates.append(
                ExtractedChargeCandidate(
                    code=match.group("code"),
                    amount_text=match.group("amount").replace(",", "."),
                    currency=match.group("currency"),
                ),
            )
            consumed.append(match.group(0))

        remainder = input_text
        for fragment in consumed:
            remainder = remainder.replace(fragment, " ", 1)
        unparsed = [part.strip() for part in re.split(r"[\n;]+", remainder) if part.strip()]

        return ExtractionPayload(
            source_ref=source_ref.strip(),
            unparsed_regions=unparsed,
            candidates=candidates,
        )
