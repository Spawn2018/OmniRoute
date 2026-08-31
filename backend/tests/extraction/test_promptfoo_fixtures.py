"""Fixture’e promptfoo — ten sam schemat co MockExtractor; CI eval = echo, nie LLM."""

from pathlib import Path

from app.ai_transforms.extraction.mock_extractor import MockExtractor

# Zsynchronizowane z promptfoo/promptfoo.yaml (vars.document).
PROMPTFOO_FIXTURES: tuple[tuple[str, str], ...] = (
    ("doc://promptfoo/thc", "THC 100 EUR"),
    ("doc://promptfoo/baf", "BAF 12 USD; weekend note"),
)

_REPO_ROOT = Path(__file__).resolve().parents[3]


def test_promptfoo_fixtures_match_extraction_schema() -> None:
    extractor = MockExtractor()
    for source_ref, document in PROMPTFOO_FIXTURES:
        payload = extractor.extract(source_ref=source_ref, input_text=document)
        dumped = payload.model_dump()
        assert dumped["source_ref"] == source_ref
        assert isinstance(dumped["unparsed_regions"], list)
        assert isinstance(dumped["candidates"], list)
        for candidate in dumped["candidates"]:
            assert "amount_text" in candidate
            assert "code" in candidate
            assert len(candidate["currency"]) == 3


def test_promptfoo_yaml_lists_same_documents() -> None:
    yaml_text = (_REPO_ROOT / "promptfoo" / "promptfoo.yaml").read_text(encoding="utf-8")
    for _source_ref, document in PROMPTFOO_FIXTURES:
        assert document in yaml_text

