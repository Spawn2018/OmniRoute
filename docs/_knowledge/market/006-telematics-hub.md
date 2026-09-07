# Omni Telematics Hub (decyzja 2026-09-07)

**Kiedy:** Plan V5 / V5b. Zero własnego HW. Szczegóły i listy: `docs/analysis/benchmark-tms-2026.md` §13g.

## Źródła pozycji (kolejność)

1. Teltonika / Queclink — pakiet Omni u przewoźnika, który chce.
2. BYO API — poświadczenia tenanta + płyta → `resource`.
3. Aggregator (Linkway / DRIP) gdy brak native adaptera.
4. Giełda: Trans.eu `/monitoring`+`/trace`, TIMOCOM Tracking, Transporeon Visibility — per transport.
5. Driver app / SMS geo (zgoda) — poziom 0.

## Okno obserwacji (decyzja operatora 2026-09-08)

| Rodzaj | Zasada |
|---|---|
| `omni_telematic` | Pakiet Omni u przewoźnika + umowa powierzenia → wolno pollować **flotę**. |
| `external_api` | Start przy `trip`. Stop: **3 dni robocze** bez zlecenia na tej płycie. Nowy trip = znów `active`. |

Historia zostaje w `entity_event`. Kalendarz dni roboczych = dane tenanta (nie „3 noce”).

## P0 adaptery PL

IKOL `iaGetLocatorLastPosition` · Flotis REST positions · GBOX (docs.gbox.pl) · Wialon SDK.

Tronik ATRAX4, Logisat — API po umowie; Linkway może już mieć ATRAX4. Native dopiero po dokumentacji; do tego czasu L1c. Reszta listy PL/EU: aggregator albo na żądanie.

## Giełdy — czat

Wolno: wiadomości, w których tenant jest stroną (API/eksport) → HITL → `rate_line`.  
Nie wolno: scraping komunikatora. Diagnostyka spedytora = metryki jobu + accepted price API + `quoted_amount` na M-30.

## Zakazy

Własny firmware. Poll floty na **zewnętrznym** GPS poza oknem 3 dni roboczych. Hasła w logach. LLM liczący ETA.
