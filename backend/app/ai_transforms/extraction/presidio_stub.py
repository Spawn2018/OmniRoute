"""Presidio na ścieżce instructor — stub, nie żywy analyzer na każdym endpoincie.

Cel HC (microsoft-presidio + wszystkie trasy) = nie ten plaster.
Wyjątek podaje etykietę encji, nigdy dopasowany tekst.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.domain.errors import UntrustedExtractionInput

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
# Wymaga prefiksu + — same cyfry z cennika (THC 125.50) nie są telefonem.
_PHONE = re.compile(r"\+\d{2}\s?\d{3}[\s-]?\d{3}[\s-]?\d{3}\b")


@dataclass(frozen=True)
class PresidioFinding:
    entity_type: str
    start: int
    end: int


class InstructorPresidioStub:
    """Kontrakt analyze/scan jak Presidio Analyzer — bez pakietu microsoft-presidio."""

    engine = "stub"

    def analyze(self, text: str) -> list[PresidioFinding]:
        findings: list[PresidioFinding] = []
        for match in _EMAIL.finditer(text):
            findings.append(PresidioFinding("EMAIL_ADDRESS", match.start(), match.end()))
        for match in _PHONE.finditer(text):
            findings.append(PresidioFinding("PHONE_NUMBER", match.start(), match.end()))
        return findings

    def scan(self, prompt: str) -> None:
        findings = self.analyze(prompt)
        if not findings:
            return
        labels = sorted({finding.entity_type for finding in findings})
        raise UntrustedExtractionInput(
            f"Wejście odrzucone przez skaner presidio_stub ({', '.join(labels)})",
        )
