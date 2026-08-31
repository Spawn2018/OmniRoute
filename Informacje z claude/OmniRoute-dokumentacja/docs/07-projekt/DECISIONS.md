---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
---

# Rozstrzygnięcia

Jedna linia na decyzję. Agent czyta przed zadaniem pytania, które już padło.

| Data | Pytanie | Rozstrzygnięcie |
|---|---|---|
| 2026-08-29 | Nazwa produktu | OmniRoute |
| 2026-08-29 | Podmiot sprzedający | LOGMAR Sp. z o.o. |
| 2026-08-29 | Kolejność rynków | morze → droga → lotnictwo |
| 2026-08-29 | Zasięg sprzedaży | Polska i zagranica |
| 2026-08-29 | Hosting produkcyjny | Hetzner, Niemcy |
| 2026-08-29 | Zespół | jednoosobowy przez najbliższy rok |
| 2026-08-29 | Event sourcing | nie — outbox plus audit_log. ADR-001 |
| 2026-08-29 | Kaskada narzutów w SQL czy w Pythonie | Python — mały zbiór |
| 2026-08-29 | Ocena kredytowa dla działalności jednoosobowych | bez punktacji, tylko dane |
| 2026-08-29 | Faktoring własny | nie — pośrednictwo, partner zewnętrzny |
| 2026-08-29 | Wyłączność dla faktora | tak, umowa w przygotowaniu |
| 2026-08-29 | Mikroserwisy | nie — modularny monolit |
| 2026-08-29 | Zespół agentów z personami | nie — orkiestrator z subagentami |
| 2026-08-29 | Metodyka | przepływ z limitem 1, delta-spec, praktyki XP |
| 2026-08-29 | Rozliczenie z klientami | za użytkownika, nigdy za przesyłkę |
| 2026-08-29 | Cennik publiczny | tak — przewaga w 2026 |

## Otwarte

| # | Pytanie | Termin |
|---|---|---|
| O-01 | Osobny podmiot na produkt w przyszłości? | przy piątym kliencie |
| O-04 | Dostawca księgowości do integracji | przed plastrem 6.4 |
| O-05 | Agregator stawek | gdy klienci zapłacą |
| O-08 | Model prowizji faktoringowej | przed plastrem 9.22 |
| O-09 | Udział w dyskoncie | przed plastrem 9.19 |
| — | Sąd rejestrowy i kapitał zakładowy do umów | przed pierwszą umową |
| — | Kancelaria do weryfikacji dokumentów | przed pierwszą umową |
| — | Ubezpieczenie OC działalności IT | przed pierwszym klientem |
