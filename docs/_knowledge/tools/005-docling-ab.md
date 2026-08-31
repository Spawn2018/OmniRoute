# Docling A/B (0.9)

**Kiedy:** ingest PDF / bajtów przed HITL

1. `layout_fingerprint` — pdf vs text.
2. Parser A: deterministyczny (`stub` / `pdf_strings`).
3. Parser B: docling (opcjonalny pakiet).
4. Tryb `ab`: wygrywa dłuższy tekst; zapisz `ab_delta_chars`.
5. CI: `EXTRACTION_PARSER=stub`. Nie ładuj docling do kontekstu.

Kod: `backend/app/integrations/docling/`
