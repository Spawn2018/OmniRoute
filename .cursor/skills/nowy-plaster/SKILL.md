---
name: nowy-plaster
description: Pełna procedura pionowego plastra od migracji do komponentu
---

# Pionowy plaster

Kolejność jest obowiązkowa. Nie przeskakuj etapów.

## 0. Przygotowanie
- `python scripts/quality/factory_cycle.py --start plaster` — retrieve + podłoga + delta produktu w `docs/deltas/open/` (nie `OS-*`). Brak delty = stop.
- Przeczytaj `docs/state/CURRENT.md` i delta-spec.
- Jeśli poprzedni plaster ma niezacommitowany / niepushnięty WIP — **stop**, domknij go.
- Sprawdź `docs/PLAN-REALIZACJA.md` § Gate dziś vs DoD (co jest stubem).
- Uruchom `lowca-duplikatow`.
- Jeśli `CURRENT.md` mówi **Etap: Plan** albo pozycja kolejki to nowa wydmuszka M-xx: **stop** — najpierw `/plan-modul` (tryb Plan w Cursorze), zero kodu. **Wyjątek `/noc`:** nie stop i nie tryb Plan — wykonaj plan-modul w Agencie wg `docs/ops/nocna-zmiana.md`, potem ten plaster.
- **Plan przed kodem** przy >3 plikach — także poza kolejką. Czekaj na akceptację. **Wyjątek `/noc`:** nie czekaj; testy, kod, push, pętla.
- Kolejka „co dalej” jest w `docs/PLAN-REALIZACJA.md`, nie w pamięci operatora.
- Po akceptacji, osobna tura: `/testy` (czerwone testy z delty, bez implementacji).
  Ten sam przebieg nie pisze testów i kodu.

## 1. Migracja
- sprawdź aktualny schemat w `backend/alembic/versions/` (ta tabela) i w modelach tego BC
- `organization_id`, `created_at`, `updated_at`, `created_by` w każdej tabeli
- polityka RLS + FORCE ROW LEVEL SECURITY
- kwoty: `Numeric(14,4)` + `CHAR(3)` waluta obok
- `just migrate-down` musi przejść

## 2. Model → 3. Repozytorium → 4. Serwis → 5. Endpoint
- Zgodnie z `.cursor/rules/backend.mdc`
- Outbox **gdy są zdarzenia między modułami** — nie pisz outbox „na zapas”

## 6. Typy frontendu
- `just api-types` (openapi-ts) — katalog `frontend/src/api/` tylko do odczytu.
- Gate: typecheck, nie regen. Nie edytuj wygenerowanych plików.
- Dług: generator spłaszcza `ExtractRequest` anyOf|null — wrapper `as ExtractRequest`.

## 7. Komponent
- `features/<moduł>/`, TanStack Query, `<Money/>`
- Listy: wyłącznie DataTableShell (ADR-0002)
- DNA wizualne (tylko wygląd): otwórz `docs/design/omniroute-briefing-mockup.html` — ekrany **Wyceny** i **Zlecenia**. Kolory wyłącznie tokenami z `frontend/src/index.css` (nie hardcode OKLCH). Spacing / padding / radius / typografia jak w mockupie: `rounded-md`, panele `p-3` + `outline` 1px `border`, powierzchnia `p-4 gap-4`, kontrolki `h-8`, body `text-sm`, meta/tabela `text-xs`. Żywy kod wzorca: `frontend/src/features/quotations/catalog-page.tsx` i `frontend/src/features/shipment/catalog-page.tsx`.
- Zakaz: kopiowanie HTML mockupu do `frontend/`; `docs/design/omniroute-ui.html` (sprzedaż, hue-165); paleta `docs/design/app-preview.html` (hue 250); Watchtower / mapa z mockupu; `sum()` w JS.

## 8. Testy z `/testy` muszą przejść
- hypothesis dla reguł biznesowych i izolacja tenantów — z tury `/testy`
- Vitest: DataTableShell + `extractionCreateBody` + `hitlSplitView`. PDF canvas HITL — brak.

## Definicja ukończenia
`just gate` zielone (tylko realne kroki, nie `echo`) + pętla `docs/ops/post-plaster.md` + człowiek + delta zarchiwizowana + **push**.
Zamknięcie: skill `zamknij-plaster`.
