# Przyjęcie RFP

Na `/tender-rfp-intakes` zapisujesz **przyjęcie RFP** przy istniejącym nagłówku przetargu. To HITL operatora: nic z modelu językowego nie wchodzi tu samo. Auto-award zostaje leftover.

1. Wejdź na Przyjęcie RFP. Wklej `tender_id` nagłówka tenanta.
2. Podaj kod przyjęcia (snake, np. `scope`).
3. „Zapisz przyjęcie” z `source_ref` (`fixture://tender-rfp-intake/…` albo `tenant:manual`).

Czego tu nie ma: zapis z LLM, `draft_kind=tender_rfp`, auto-award, TED, kwota na tym wierszu, suma w przeglądarce. Szkic extractu zostaje na `/ai`. Marża zostaje na `/charges`. Nagłówek zostaje na `/tenders`.

Nazwy w kodzie: `tender_rfp_intake` · `tender_id` · `intake_code` · `source_ref`.
