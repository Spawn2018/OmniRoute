from app.ai_transforms.extraction.mock_extractor import MockExtractor


def test_mock_extractor_requires_source_ref_and_unparsed() -> None:
    extractor = MockExtractor()
    payload = extractor.extract(
        source_ref="tariff://demo-2026",
        input_text="THC 125.50 EUR\nnote: weekend surcharge\nBAF 12 USD",
    )
    assert payload.source_ref == "tariff://demo-2026"
    assert len(payload.candidates) == 2
    assert payload.candidates[0].code == "THC"
    assert payload.candidates[0].amount_text == "125.50"
    assert payload.candidates[0].currency == "EUR"
    assert any("weekend" in region.lower() for region in payload.unparsed_regions)
