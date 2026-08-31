from app.integrations.docling.parser import StubDocumentParser
from app.integrations.langfuse.tracer import build_langfuse_tracer


def test_stub_document_parser_decodes_utf8() -> None:
    parsed = StubDocumentParser().parse(source_ref="doc://x", raw_bytes=b"THC 1 EUR")
    assert parsed.text == "THC 1 EUR"
    assert parsed.parser_name == "stub"


def test_langfuse_tracer_disabled_without_keys() -> None:
    tracer = build_langfuse_tracer()
    assert tracer.enabled is False
    trace = tracer.start_trace("extract")
    trace.update(tokens=1)
    trace.end()
    assert trace.name == "extract"
