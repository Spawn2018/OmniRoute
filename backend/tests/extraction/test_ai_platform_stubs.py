import pytest

from app.domain.errors import ExtractionProviderUnavailable
from app.integrations.docling.parser import StubDocumentParser
from app.integrations.langfuse.tracer import LangfuseTracer, PromptTrace, build_langfuse_tracer


def test_stub_document_parser_decodes_utf8() -> None:
    parsed = StubDocumentParser().parse(source_ref="doc://x", raw_bytes=b"THC 1 EUR")
    assert parsed.text == "THC 1 EUR"
    assert parsed.parser_name == "stub"


def test_langfuse_tracer_disabled_without_keys() -> None:
    tracer = build_langfuse_tracer()
    assert tracer.enabled is False
    trace = tracer.start_trace("extract")
    trace.update(tokens=1)
    tracer.finish(trace)
    assert trace.name == "extract"


def test_langfuse_push_requires_package_when_enabled(monkeypatch: pytest.MonkeyPatch) -> None:
    real_import = __import__

    def blocked(
        name: str,
        globals: object = None,
        locals: object = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> object:
        if name == "langfuse" or name.startswith("langfuse."):
            raise ImportError("test: pakiet niedostępny")
        return real_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr("builtins.__import__", blocked)
    tracer = LangfuseTracer(enabled=True)
    trace = PromptTrace("extract")
    trace.update(source_ref="doc://x")
    with pytest.raises(ExtractionProviderUnavailable):
        tracer.finish(trace)
