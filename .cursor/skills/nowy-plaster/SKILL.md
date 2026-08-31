---
name: nowy-plaster
description: Pełna procedura pionowego plastra od migracji do komponentu
---

# Pionowy plaster

Kolejność jest obowiązkowa. Nie przeskakuj etapów.

## 0. Przygotowanie
- Przeczytaj `docs/state/CURRENT.md` i delta-spec.
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
- `just api-types` — nigdy ręcznie

## 7. Komponent
- `features/<moduł>/`, TanStack Query, `<Money/>`

## 8. Test
- hypothesis dla reguł biznesowych
- izolacja tenantów dla nowych tabel

## Definicja ukończenia
`just gate` zielone + weryfikator + delta-spec zarchiwizowana.
