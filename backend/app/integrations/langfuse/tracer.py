"""Langfuse — no-op gdy brak kluczy; pakiet tylko gdy enabled."""

from app.core.config import settings
from app.domain.errors import ExtractionProviderUnavailable


class PromptTrace:
    def __init__(self, name: str) -> None:
        self.name = name
        self.metadata: dict[str, str | int] = {}

    def update(self, **fields: str | int) -> None:
        self.metadata.update(fields)

    def end(self) -> None:
        return None


class LangfuseTracer:
    """Telemetria promptów — bez sieci i bez input_text gdy wyłączone."""

    def __init__(self, *, enabled: bool) -> None:
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    def start_trace(self, name: str) -> PromptTrace:
        return PromptTrace(name)

    def finish(self, trace: PromptTrace) -> None:
        if self._enabled:
            self._push(trace)
        trace.end()

    def _push(self, trace: PromptTrace) -> None:
        try:
            from langfuse import Langfuse
        except ImportError as exc:
            raise ExtractionProviderUnavailable(
                "LANGFUSE_PUBLIC_KEY ustawiony — zainstaluj pakiet langfuse",
            ) from exc

        client = Langfuse(
            public_key=settings.langfuse_public_key,
            secret_key=settings.langfuse_secret_key,
            host=settings.langfuse_host,
        )
        client.trace(name=trace.name, metadata=dict(trace.metadata))
        client.flush()


def build_langfuse_tracer() -> LangfuseTracer:
    enabled = bool(settings.langfuse_public_key and settings.langfuse_secret_key)
    return LangfuseTracer(enabled=enabled)
