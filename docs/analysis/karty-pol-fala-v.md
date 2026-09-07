# Karty pól — Fala V + B0b (predykcje / telematyka / wieża) — SZKIC do `/plan-modul`

**Zależności:** B0a (`entity_event`) przed O; T1–T2 przed actuals TT i oknem GPS; V1 przed ETA. AIS wieży = leftover S32, **nie** V5.  
**Pola:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md) §2–3, §3.8 pogoda.

## B0b (po T2)

| Tabela | Pola (szkic) | Uwagi |
|---|---|---|
| `prediction_ledger` | predykcja, horyzont, MAE/CRPS po fakcie, `source_ref` | bez metryki = zakaz „AI przewiduje” |
| `plan_snapshot` | zlecenie→trip→zasób, autor, czas | wersje planu |
| indeks paliwa | obok `nbp_rate` | nie `rate_line` |
| własne TT | z `stop.actual_*` | nie O1 `transit_days` oferty |

## Fala V

| ID | Tabele / pola | Uwagi |
|---|---|---|
| V1 | `prediction_ledger` + scorecard | champion/challenger, drift |
| V2 | ETA planned/historical/live/risk-adjusted; `weather_observation` wzdłuż `trip.route_geometry` | Open-Meteo; SaaS = plan płatny albo AGPL; nie LLM |
| V2b | myto → `charge` + `source_ref`; klasa/osie z `resource` | brak taryfy = warning; P0 leftover najpierw |
| V3 | D&D watchdog; rollover ETD/ETA | morze; blank sailing = HZ/V1 |
| V4 | AIS na wieży | leftover S32; lazy chunk |
| V5 | `position_event`; `telematics_connector`; `resource_telematics_link.observation_kind` | `omni_telematic` = poll floty (pakiet Omni + umowa). `external_api` = 3 **dni robocze** bez trip → stop; nowy trip → active. P0 GBOX/IKOL/Flotis/Wialon. Zero własnego HW |
| V5b | `exchange_message` gdy tenant stroną; `quoted_amount` na inquiry | oficjalne API; zakaz scrapingu czatu |
| V6 | łańcuch stock→produkcja→sprzedaż→EBITDA; „co jeśli” | ui-06; nie scoring osoby |
| V7 | tacho / czas pracy / prom art. 9 | TO_VERIFY prawo; apka nie poprawia DDD |
| V8 | what-if na B0 | po V6; linie NO/DE/SE = dane, nie magia |

8 twinów PDF (pojazd/kierowca/kontener jako pełna symulacja) = HZ, nie V1.
