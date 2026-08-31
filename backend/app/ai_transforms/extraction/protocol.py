from typing import Protocol

from app.ai_transforms.extraction.schemas import ExtractionPayload


class DocumentExtractor(Protocol):
    def extract(self, *, source_ref: str, input_text: str) -> ExtractionPayload:
        """Zwraca Intent payload — zapis domenowy tylko przez service + HITL."""
        ...
