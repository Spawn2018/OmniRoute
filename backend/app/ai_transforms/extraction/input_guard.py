"""Skanery wejścia w kontrakcie llm-guard — bez modelu ML w CI.

Pełny pakiet `llm-guard` (transformers) jest opcjonalny: EXTRACTION_LLM_GUARD=true
i `pip install llm-guard`. Domyślnie działają skanery regex (injection + sekrety).
"""

from __future__ import annotations

import re
from typing import Protocol

from app.core.config import settings
from app.domain.errors import ExtractionProviderUnavailable, UntrustedExtractionInput

_INJECTION = re.compile(
    r"(ignore previous instructions|disregard all rules|you are now |jailbreak|"
    r"reveal (your |the )system prompt)",
    re.IGNORECASE,
)
# Wzorce sekretów — wyjątek podaje nazwę skanera, nigdy dopasowany tekst.
_SECRETS = re.compile(
    r"(sk-[A-Za-z0-9]{10,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|"
    r"Bearer [A-Za-z0-9\-._~+/]+=*)",
)


class InputScanner(Protocol):
    name: str

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        """Jak llm-guard: (sanitized, is_valid, risk_score)."""
        ...


class InjectionScanner:
    name = "prompt_injection"

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        if _INJECTION.search(prompt):
            return prompt, False, 1.0
        return prompt, True, 0.0


class SecretsScanner:
    name = "secrets"

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        if _SECRETS.search(prompt):
            return prompt, False, 1.0
        return prompt, True, 0.0


class ExtractionInputGuard:
    def __init__(self, scanners: list[InputScanner] | None = None) -> None:
        self._scanners = scanners or [InjectionScanner(), SecretsScanner()]

    def scan(self, prompt: str) -> None:
        for scanner in self._scanners:
            _sanitized, is_valid, _risk = scanner.scan(prompt)
            if not is_valid:
                raise UntrustedExtractionInput(
                    f"Wejście odrzucone przez skaner {scanner.name}",
                )
        if settings.extraction_llm_guard:
            self._scan_llm_guard_package(prompt)

    def _scan_llm_guard_package(self, prompt: str) -> None:
        try:
            from llm_guard.input_scanners import BanSubstrings
        except ImportError as exc:
            raise ExtractionProviderUnavailable(
                "EXTRACTION_LLM_GUARD=true wymaga pakietu llm-guard",
            ) from exc

        scanner = BanSubstrings(substrings=["ignore previous instructions"])
        _sanitized, is_valid, _risk = scanner.scan(prompt)
        if not is_valid:
            raise UntrustedExtractionInput("Wejście odrzucone przez skaner llm_guard")
