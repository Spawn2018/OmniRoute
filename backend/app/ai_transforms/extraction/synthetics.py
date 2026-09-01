"""Syntetyki extract/eval — 8–12 tekstów. Zero PDF klienta, zero PII."""

from __future__ import annotations

# source_ref synth://… + tekst cennika. Kwoty jako tekst; LLM nie liczy.
SYNTHETIC_DOCUMENTS: tuple[tuple[str, str], ...] = (
    ("synth://thc-alpha", "THC 125.50 EUR"),
    ("synth://baf-weekend", "BAF 12 USD; dopłata weekendowa fikcyjna"),
    ("synth://caf-note", "CAF 3.5 EUR\nwarunki: umowa ramowa syntetyczna"),
    ("synth://thc-baf-pair", "THC 80 EUR\nBAF 15 EUR"),
    ("synth://isps-comma", "ISPS 25,00 EUR"),
    ("synth://doc-ohc", "DOC 45 USD\nOHC 20 USD"),
    ("synth://lss-pl", "LSS 8 EUR\nnota: terminal syntetyczny A"),
    ("synth://pss-footer", "PSS 6 USD; stopka nierozpoznana xyz"),
    ("synth://wrs-dhc", "WRS 4 EUR\nDHC 30 EUR"),
    ("synth://unparsed-only", "uwaga operatora: brak stawki w tym akapicie"),
)
