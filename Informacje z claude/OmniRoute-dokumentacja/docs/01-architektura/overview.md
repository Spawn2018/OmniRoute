---
status: aktualny
owner: Sebastian Bożek
last_review: 2026-08-29
next_review: 2026-11-29
---

# Architektura OmniRoute

## Kształt systemu

Modularny monolit z granicami wymuszanymi przez `import-linter`.
Nie mikroserwisy — przy jednej osobie rozproszenie mnoży problemy operacyjne
bez korzyści.

```
api → services → repositories → models
workflows → services
integrations → domain     (nigdy do services)
domain → (nic zewnętrznego)
```

## Mapa katalogów

| Ścieżka | Zawartość | Kto importuje |
|---|---|---|
| `backend/app/api/` | routery, DTO | — |
| `backend/app/workflows/` | Temporal | — |
| `backend/app/services/<moduł>/` | logika domenowa | api, workflows |
| `backend/app/repositories/` | dostęp do danych | services |
| `backend/app/models/` | SQLAlchemy | repositories |
| `backend/app/domain/` | typy, wyjątki, wartości | wszyscy |
| `backend/app/integrations/` | adaptery zewnętrzne | api, workflows |
| `frontend/src/features/<moduł>/` | pion modułu | — |
| `frontend/src/components/ui/` | shadcn, skopiowane | features |
| `frontend/src/api/` | generowane z OpenAPI | features, tylko odczyt |

## Moduły domenowe niezależne

`rates` · `quotation` · `rfq` · `shipment` · `finance` · `compliance` ·
`extraction` · `carrier` · `platform`

Komunikacja wyłącznie przez outbox. Nazewnictwo zdarzeń:
`modul.zdarzenie_w_czasie_przeszlym`.

## Stos

```
DANE       PostgreSQL 16 + RLS + pgvector + pg_trgm
           replika odczytu · Redis · MinIO
           ścieżka do Citus przy shardingu po organization_id
PROCESY    Temporal (workflow z timerami) · Hatchet (zadania per tenant)
           procrastinate (cykliczne) · outbox (zdarzenia domenowe)
API        FastAPI + granian · SSE do strumieniowania wycen · OpenFGA
AI         instructor + Claude API · llm-guard · langfuse · promptfoo
FRONT      Vite SPA + TanStack + shadcn + Tailwind v4 (OKLCH)
           portal klienta i przewoźnika jako osobne aplikacje
OBSERW.    OpenTelemetry → Sentry · Grafana · PostHog · Langfuse
```

## Czternaście zasad

1. `organization_id` w każdej tabeli, RLS wymuszany przez bazę
2. Konfiguracja jest danymi, nie kodem
3. `charge` to jedyne miejsce prawdy o marży
4. Model wyciąga dane, kod je przetwarza — model nigdy nie liczy
5. Każda stawka ma `source_ref`
6. Stawki niemutowalne po pierwszym użyciu w ofercie
7. Kwoty jako `Decimal`, waluta nierozerwalnie z kwotą
8. Nic z ekstrakcji nie wchodzi bez akceptacji człowieka
9. Poświadczenia zewnętrzne należą do tenanta
10. Wszystko z zewnątrz jest niezaufane
11. Nie licz w Pythonie tego, co Postgres policzy z indeksem na dużym zbiorze
12. Żadne zapytanie nie sięga po dane więcej niż jednego tenanta
13. Każde wywołanie zewnętrzne idempotentne, każde zdarzenie przez outbox
14. Zanim napiszesz funkcję, sprawdź, czy istnieje

## Ścieżka skalowania

| Poziom | Kiedy | Jak |
|---|---|---|
| Wspólny schemat + RLS | domyślnie | jak dziś |
| Sharding po tenancie | duży wolumen | Citus |
| Osobna baza | klient korporacyjny | routing połączenia |

Warunek: zasada 12 przestrzegana bezwyjątkowo.
