# ADR-0003: System UI OmniRoute — tokeny, primitywy, wzorce ekranów

**Status:** przyjęta  
**Data:** 2026-09-01  
**Moduły:** platforma UI (wszystkie trasy), uzupełnia [0002](0002-frontend-platform-2026.md)  
**Nie zastępuje:** ADR-0002 (stack, DataTableShell, zakaz drugiego grid engine)

## Kontekst

Badanie UI/UX (`Informacje z claude/Frontend według cloude.md`) jest dobrym przeglądem rynku (Fiori funkcjonalnie, CargoWise jako antywzorzec, OKLCH, HAX G10, EAA) i słabą specyfikacją produktu: pisze tak, jakby frontend nie istniał, i pomija wzorce rdzenia OmniRoute (HITL, `superseded_by`, `source_ref`, `charge` = marża, tenant w shellu).

Stan kodu 2026-09-01: AppShell + DataTableShell (compact/comfortable) + ⌘K + IBM Plex Sans + `tabular-nums` + `<Money amount: string/>`. Brak: OKLCH, tryb ciemny, condensed, wyrównanie kwot do przecinka, `components.json`, i18n, Playwright/axe, print.

Makiety: [docs/design/](../design/README.md) (kopia w git) oraz katalog Canvas IDE (podgląd obok czatu). Nie wchodzą do bundla `frontend/`.

## Decyzja

### 1. Primitywy: Radix, nie Base UI

Zostajemy na Radix (stan B.5). shadcn/ui od lipca 2026 init-uje Base UI; Radix jest wspierany. W `frontend/components.json` jawny base **radix** (`-b radix` przy CLI). Migracja na Base UI tylko nowym ADR. Zakaz dwóch bibliotek primitywów w jednym drzewie.

### 2. Tokeny: OKLCH luminance-first + dark od razu

Migracja hex w `frontend/src/index.css` → OKLCH. Kanał L = motyw/kontrast, C = emfaza, H = marka (zieleń spedycyjna, nie fiolet). Motyw jasny i ciemny w tej samej palecie. Bramka: test par tokenów ≥ 4.5:1 (WCAG 2.2 AA). `prefers-color-scheme` + przełącznik w shellu. `prefers-reduced-motion` honorowane (EN 301 549 klauzula 9.7 — preferencje użytkownika; v4.1.1 cytowanie OJ planowane ~30.11.2026; do cytowania obowiązuje v3.2.1 / WCAG 2.1 AA — celujemy 2.2 AA proaktywnie).

Usunąć ręczną klasę `.tabular-nums` z CSS — Tailwind v4 ma utility.

### 3. Gęstość: trzeci tryb tylko na gridzie stawek

| Tryb | Gdzie |
|---|---|
| comfortable | shell, formularze, HITL, touch |
| compact | domyślny desktop (już jest) |
| condensed | wyłącznie DataTableShell katalogu `rate_line` / dużych list stawek |

Nie globalny condensed na cały layout. Nadal jeden silnik: TanStack Table + Virtual. Kopiujemy zachowania Fiori (freeze, próg virtualizacji, edycja w miejscu jako nowy rekord), nie cztery komponenty tabeli.

### 4. Money: wyrównanie do przecinka

`<Money/>` zostaje na `amount: string`. Docelowo: `lining-nums tabular-nums`, siatka integer / fraction / kod ISO 4217, locale formatuje grupowanie. Max 4 miejsca (kanon). Optymistyczna aktualizacja **zakazana** na kwocie, `rate_line`, `accept`.

### 5. Pozycjonowanie: natywny CSS Anchor + Popover API

Tooltip, menu, popover: `anchor-name` / `position-anchor` + Popover API (Baseline 2026, Firefox 147). Floating UI tylko za `@supports` jako fallback. Cel: nie dociągać Floating UI do initial chunka (budżet 250 kB gzip).

View Transitions: same-document, master→detail, za `prefers-reduced-motion`. Container queries: gęstość/układ HITL per panel, nie globalny breakpoint.

### 6. Mapa: leniwy chunk, własny budżet

Watchtower / mapa **nie** w Fali 1 i **nie** w initial JS. Zależne od M-05 (geografia) i Fali 5 (zlecenie/tracking). Chunk trasy z własnym limitem; `just perf` nadal mierzy tylko wejście.

### 7. i18n: struktura tak, tłumaczenia nie

Teksty przez warstwę kluczy od pierwszego plastra UI po tym ADR. Jeden język w paczce (pl). Format dat/kwot z locale. Zakaz hardcoded stringów w nowych ekranach. Drugi język = osobny plaster, nie ten ADR.

### 8. Testy UI jako gate (kolejka, nie teraz)

Playwright: trzy ścieżki krytyczne (sesja → lista stawek; HITL accept; wycena). axe-core na każdej trasie. Nie zamyka Q1. Vitest logiki zostaje.

### 9. Wzorce, których badanie nie opisało (obowiązkowe w UI)

- HITL: confidence per pole, span w PDF, draft → accept, odrzucenie z powodem, Art. 50 na recenzji. Optimistic accept zakazany.
- `rate_line`: niemutowalność; edycja = nowy wiersz + `superseded_by`.
- `source_ref` klikalny z wiersza; brak pochodzenia = brak zapisu.
- `charge`: kupno, sprzedaż, marża w jednym wierszu; `margin()` serwer.
- Tenant zawsze w shell barze. OpenFGA: brak relacji = ukryj; read-only = wyszarzyj + 403 z uzasadnieniem; nie 404-teatr.
- Print: arkusze B/L / FV / list przewozowy — leftover `U-print`, nie teraz.

### 10. Optimistic UI — rozróżnienie

| Wolno (natychmiast) | Zakazane |
|---|---|
| filtr, kolejność kolumn, zapis widoku | kwota, `charge`, `rate_line`, accept HITL |

## Rozważane alternatywy

| Alternatywa | Werdykt |
|---|---|
| Cztery typy tabel Fiori jako cztery komponenty | odrzucone — ADR-0002, jeden silnik |
| Base UI teraz (domyślny shadcn 2026-07) | odrzucone — koszt migracji, dwa primitywy |
| Watchtower w MVP / Q1 | odrzucone — brak backendu, rozsadza 250 kB |
| Optimistic na stawkach | odrzucone — zasady 7–8 |
| HEX + jeden motyw, dark „później” | odrzucone — 9.7 + procurement EAA |
| i18n z pełnym EN od dnia 1 | odrzucone — struktura wystarczy; drugi język to plaster |

## Konsekwencje

- Zero kodu w `frontend/` w tym ADR. Implementacja = leftovery **U-oklch-dark**, **U-money-align**, **U-condensed**, **U-primitives-json**, **U-i18n-structure**, **U-playwright-axe**, **U-print** w [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) — **poza** kolejką Q1.
- Wizja (canvas 06) zależy od M-05 + M-35–M-37 + M-61+. Nie claim „powierzchnia 2026”.
- CLI shadcn bez `-b radix` = błąd procesu (wciągnie Base UI).
- DoD merge: ADR-0002 (silnik tabeli) **i** ten dokument (tokeny, Money, HITL, tenant).

## Źródła

| Źródło | Wniosek użyty |
|---|---|
| Badanie Claude 2026-09 (archiwum, nie kanon) | Fiori funkcjonalnie; CargoWise antywzorzec; HAX G10 |
| [shadcn changelog 2026-07 Base UI default](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default) | Radix zostaje; pin w components.json |
| EN 301 549 v3.2.1 dziś; v4.1.1 draft / cytowanie OJ ~XI 2026 | cel WCAG 2.2 AA; klauzula 9.7 |
| CSS Anchor Positioning Baseline (Firefox 147, I 2026) | bez Floating UI w initial |
| ADR-0002 | jeden DataTableShell |
| GROUNDING / 13 zasad | tenant, Decimal, HITL, source_ref, charge |
