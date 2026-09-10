# Mapa funkcji konkurencji — 2026-09

**Nie dump wiki.** Kanon kolejki: [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Oś leftoverów `/noc`. Benchmark SPEED/Qargo: [benchmark-tms-2026.md](benchmark-tms-2026.md).

Omni = **OS spedytora**: job jak CargoWise, ślad jak FourKites (nie autonomia Loft), widoczność XOR, what-if na kopii planu (kształt Kinaxis, nie ich silnik in-memory). Nie WMS (EXP8).

## Co bierzemy (kształt), czego nie klonujemy

| Źródło | Bierzemy | Nie klonujemy |
|---|---|---|
| CargoWise | Job / file: jedna sprawa, dokumenty, strony, cutoffy na obiekcie | Desktop-era UI, T-SQL u klienta, wszystko-w-jednym ekranie |
| p44 / FourKites / Shippeo | Zdarzenie + mileston na zleceniu; jeden dostawca na tenant | Trzy feedy naraz; scoring kierowcy; „AI ETA” z modelu |
| Kinaxis | Gałąź planu (rodzic = żywe wiersze, dziecko = `plan_snapshot`) | Maestro S&OP fabryki; in-memory constraint solver |
| Blue Yonder | Wieża skutków (plan vs fakt), później load | WMS, automatyczny VRP |
| Qargo | Wejście z maila, driver app **po Auth0**, FV z FK | Czat zamiast HITL; auto-send |
| interLAN SPEED | Konfiguracja jako dane, nie custom T-SQL | Parser AST WHEN/IF; rok wdrożenia jako nasz SLA |

## Bliźniak (wzorzec platformy, nie druga tabela)

Stan w RLS + `entity_event` + opcjonalnie kopia planu / karta komunikacji. Katalog W1 (osiem rodzajów) to **pierwsza** półka, nie sufit. Nie `*_twin` obok każdej tabeli. Nie `charge`, JWT, szkice, outbox.

AI **szuka i proponuje**. `operator_decision` zamyka. LLM nie liczy marży, VAT, ETA, `p_success`, VRP. Szukanie kółek = Postgres. Narracja tylko z faktów JSON.

## Komunikacja (po S53)

Źródło = skrzynka tenanta, HITL `mail_draft`. Brzmi jak **ten pracownik × ten odbiorca** (diada), nie jak cudzy klient ani armator. Art. 50. RODO M-56. Bez Graph/SMTP auto-send. ExtractionService nadal nie składa treści na ślepo — luz tylko na ścieżce HITL jak extract.

## Myto

Tenant BYO OBU/EETS → HITL mapa na `trip` → `charge` + `source_ref`. Omni nie jest e-TOLL ZSL.

## FK (P0 sekwencja, nie przed outboxem)

Optima fixture → XL → Symfonia → nexo → GT → enova/WAPRO. Nie SQL `sa`. Jeden plaster Optima na osi leftoverów; reszta w pinie.

## Uczciwość

Kinaxis wygrywa S&OP fabryki. Omni celuje w job spedytora. Qargo sprzedaje driver app + FV; Omni ma to **po** Auth0 i FK, nie zamiast cutoffów T3.
