"""Wybór ekstraktora: mock (CI) albo instructor (klucz API)."""

from app.ai_transforms.extraction.instructor_extractor import InstructorExtractor
from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.protocol import DocumentExtractor
from app.core.config import settings
from app.domain.errors import ExtractionProviderUnavailable


def default_extractor() -> DocumentExtractor:
    provider = settings.extraction_provider.strip().lower()
    if provider == "mock":
        return MockExtractor()
    if provider == "instructor":
        return InstructorExtractor.from_settings()
    raise ExtractionProviderUnavailable(f"Nieznany extraction_provider: {provider}")
