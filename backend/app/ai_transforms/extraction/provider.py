"""Instructor provider — żywy LLM w plasterze 0.8.

Do czasu 0.8 używaj MockExtractor (deterministyczny, CI-safe).
"""

from app.ai_transforms.extraction.mock_extractor import MockExtractor
from app.ai_transforms.extraction.protocol import DocumentExtractor


def default_extractor() -> DocumentExtractor:
    """Faza C hello: mock. 0.8 podmieni na InstructorExtractor + llm-guard."""
    return MockExtractor()
