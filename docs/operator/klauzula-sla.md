# Klauzula SLA (CI1)

Operator zapisuje klauzulę SLA przy istniejącej umowie klienta. To katalog HITL: kod,
metryka (`otif` / `delay` / `damage` / `other`), próg jako tekst i `source_ref`.

Nie wgrywa PDF. Nie woła LLM. Nie liczy kary. Ciphertext kary/obowiązku zostaje
leftover. Marża nadal tylko na `charge`.

Ścieżka UI: `/sla-clauses`. Najpierw musi istnieć nagłówek w `/customer-contracts`.
