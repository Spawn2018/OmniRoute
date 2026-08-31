"""InstructorExtractor — schemat Pydantic z LLM; bez sieci w testach."""

from collections.abc import Callable

from app.ai_transforms.extraction.schemas import ExtractionPayload
from app.core.config import settings
from app.domain.errors import ExtractionProviderUnavailable

CompletionFn = Callable[[str, str], ExtractionPayload]

_SYSTEM = (
    "Extract freight charge candidates from the document. "
    "Never calculate, convert, or sum amounts. "
    "Put unrecognized text in unparsed_regions. "
    "source_ref will be overwritten by the caller."
)


class InstructorExtractor:
    def __init__(self, complete: CompletionFn) -> None:
        self._complete = complete

    def extract(self, *, source_ref: str, input_text: str) -> ExtractionPayload:
        origin = source_ref.strip()
        payload = self._complete(origin, input_text)
        # HC-03: pochodzenie z żądania, model nie jest źródłem prawdy
        return payload.model_copy(update={"source_ref": origin})

    @classmethod
    def from_settings(cls) -> "InstructorExtractor":
        api_key = settings.openai_api_key.strip()
        if not api_key:
            raise ExtractionProviderUnavailable(
                "EXTRACTION_PROVIDER=instructor wymaga OPENAI_API_KEY",
            )
        return cls(complete=_openai_complete(api_key, settings.extraction_model))


def _openai_complete(api_key: str, model: str) -> CompletionFn:
    try:
        import instructor
        from openai import OpenAI
    except ImportError as exc:
        raise ExtractionProviderUnavailable(
            "instructor/openai niezaainstalowane — pip install -e '.[ai]'",
        ) from exc

    client = instructor.from_openai(OpenAI(api_key=api_key))

    def complete(source_ref: str, input_text: str) -> ExtractionPayload:
        raw = client.chat.completions.create(
            model=model,
            response_model=ExtractionPayload,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {
                    "role": "user",
                    "content": f"source_ref={source_ref}\n\n{input_text}",
                },
            ],
        )
        return ExtractionPayload.model_validate(raw)

    return complete
