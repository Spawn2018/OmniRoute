"""Langfuse — no-op gdy brak kluczy (plaster 0.10 podłączy klienta)."""

from typing import Any

from app.core.config import settings


class PromptTrace:
    def __init__(self, name: str) -> None:
        self.name = name
        self.metadata: dict[str, Any] = {}

    def update(self, **kwargs: Any) -> None:
        self.metadata.update(kwargs)

    def end(self) -> None:
        return None


class LangfuseTracer:
    """Interfejs telemetrii promptów — bez sieci gdy wyłączone."""

    def __init__(self, *, enabled: bool) -> None:
        self._enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    def start_trace(self, name: str) -> PromptTrace:
        return PromptTrace(name)


def build_langfuse_tracer() -> LangfuseTracer:
    enabled = bool(settings.langfuse_public_key and settings.langfuse_secret_key)
    return LangfuseTracer(enabled=enabled)
