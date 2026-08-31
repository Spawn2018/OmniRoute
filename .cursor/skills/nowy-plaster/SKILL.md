---
name: nowy-plaster
description: Pełna procedura pionowego plastra od migracji do komponentu
---

# Pionowy plaster

Kolejność jest obowiązkowa. Nie przeskakuj etapów.

## 0. Przygotowanie
- Przeczytaj `docs/state/CURRENT.md` i delta-spec.
- Jeśli poprzedni plaster ma niezacommitowany / niepushnięty WIP — **stop**, domknij go.
- Sprawdź `docs/PLAN-REALIZACJA.md` § Gate dziś vs DoD (co jest stubem).
- Uruchom `lowca-duplikatow`.
- Plan → akceptacja człowieka.

## 1. Migracja
- sprawdź aktualny schemat przez MCP Postgres
- `organization_id`, `created_at`, `updated_at`, `created_by` w każdej tabeli
- polityka RLS + FORCE ROW LEVEL SECURITY
- kwoty: `Numeric(14,4)` + `CHAR(3)` waluta obok
- `just migrate-down` musi przejść

## 2. Model → 3. Repozytorium → 4. Serwis → 5. Endpoint
- Zgodnie z `.cursor/rules/backend.mdc`
- Zdarzenia przez outbox

## 6. Typy frontendu
- `just api-types` (openapi-ts) — docelowo zawsze.
- Do czasu spłaty długu: tymczasowy typed klient OK, jeśli delta to dopuszcza; nie twierdź że openapi-ts jest gotowe.

## 7. Komponent
- `features/<moduł>/`, TanStack Query, `<Money/>`
- Listy: wyłącznie DataTableShell (ADR-0002)

## 8. Test
- hypothesis dla reguł biznesowych
- izolacja tenantów dla nowych tabel
- Frontend: vitest gdy delta wymaga (od 0.6 obowiązkowo dla DataTableShell)

## Definicja ukończenia
`just gate` zielone (tylko realne kroki, nie `echo`) + weryfikator + delta zarchiwizowana + **push**.
