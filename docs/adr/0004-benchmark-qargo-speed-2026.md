# ADR-0004: Benchmark Qargo/SPEED 2026 — stos zostaje, benchmark zasila kolejkę

**Status:** przyjęta (akceptacja operatora 2026-09-07)  
**Data:** 2026-09-07  
**Moduły:** kierunek produktu (wszystkie), platforma  
**Powiązane:** [0002 frontend platform](0002-frontend-platform-2026.md) · [0003 system UI](0003-frontend-ui-system-2026.md) · [PLAN-REALIZACJA](../PLAN-REALIZACJA.md)

## Kontekst

Operator dostarczył: (a) analizę Qargo TMS (qargo.com) z rekomendacją ChatGPT „przebudować na React + GraphQL + Apollo + Zustand + Ant + Django", (b) zrzuty ekranów interLAN SPEED (zlecenie drogowe, morskie, kontener, menu), (c) master-context i pełny PDF rozmowy o wizji OmniRoute (376 stron). Wykonano weryfikację źródłową: dokumentacja API i Knowledge Hub Qargo (10 twierdzeń: 9 potwierdzonych, 1 skorygowane), 59 artykułów news Qargo, 44 case studies Qargo, dossier interLAN SPEED (37 źródeł), wdrożenia SPEED i premiera iSPEED (XI 2025), 3-segmentowa analiza PDF. Surowe digesty: `docs/_source/benchmark/` (nie ładować do kontekstu). Kuracja: `docs/analysis/benchmark-tms-2026.md`.

Rekomendacja „przebudowy" była kalibrowana do statycznego mockupu HTML. Stan faktyczny repo: modularny monolit, 128 plastrów, FastAPI + React 19 + TanStack + shadcn, RLS + OpenFGA + HITL, CI gate.

## Decyzja

1. **Stos zostaje.** Zakaz przepisania na Django / GraphQL / Apollo / Zustand / Ant Design / Linaria — dopisane do anti-celów. Stack Qargo to ich historia rekrutacyjna (~2019), nie lepsza architektura; OpenAPI + openapi-ts + TanStack Query pokrywa te same potrzeby bez kosztu rewrite'u. Wniosek wzmacnia SPEED: siła = funkcje domenowe, słabość = technologia (Delphi desktop, cenniki jako ręczne procedury T-SQL, brak publicznego API); web-TMS interLAN (iSPEED) wystartował dopiero XI 2025.
2. **Benchmark zasila kolejkę.** Unia funkcjonalności trzech źródeł jest zmapowana w matrycy (`docs/analysis/benchmark-tms-2026.md`). **2026-09-08:** operator wpiął P0 + Falę O + T/D/P/X/F/C/V do `PLAN-REALIZACJA` § Kolejka; CURRENT = P0. Named parks zostają parked. `/noc` pomija parks.
3. **Karty pól standardem wejścia do Planu modułu.** Każdy nowy moduł operacyjny dostaje przed `/plan-modul` kartę pól (pole → typ → słownik → wartość domyślna → trwałość) — wzorzec: `docs/analysis/karty-pol-fala-t.md`. Zasada „wpisz raz, zapisz na stałe": słowniki per tenant, szablony, wartości domyślne (M-03), saved views (`table_view`).
4. **Gwiazda północna bez zmian:** Logistics Operating System z master-contextu (Super TMS + WMS + celny + finanse/CFO + telematyka + prediction framework + Watchtower/4PL). Statusy prawdy (`CONFIRMED/TO_VERIFY/PROPOSAL`) obowiązują — żadnych zmyślonych API, przepisów, możliwości urządzeń.
5. **Mechanizmy odrzucone świadomie** (funkcja ≠ mechanizm): konfiguracja cenników przez ręczne procedury T-SQL (u nas konfiguracja jako dane + silnik SQL), polskie nazwy kolumn w bazie, branding/kod/assety obu systemów, drugi grid engine.

## Konsekwencje

- Warstwa wykonawcza (stop → trip → resource → …) zostaje w kanonie jako **Fala T po Fali O**. S50 nadal named park (brak jobu „własne auto”); job zasobu = T2. Biurko ocean (Fala O) jest wcześniej, bo nie wymaga Auth0 ani `trip`.
- KSeF live rośnie w priorytecie (mandat PL już w mocy 2026); kalendarz regulacyjny (Peppol, CTC FR, eCMR/eFTI 2027, NIS2, CSRD) wchodzi do planowania fal F/C.
- Wieża korporacyjna z łańcuchem skutków (stock → produkcja → sprzedaż → EBITDA) potwierdzona jako wolna pozycja rynkowa — Qargo nie adresuje załadowców (przegląd 59 artykułów), SPEED nie ma warstwy predykcyjnej.
- HC bez zmian: Decimal, LLM nie liczy, HITL, `charge` = jedyna prawda o marży, RLS wszędzie, stawka bez `source_ref` nie wchodzi.

## Alternatywy odrzucone

| Alternatywa | Dlaczego |
|---|---|
| Rewrite na stack Qargo (Django/GraphQL/Apollo/Ant) | zero zysku domenowego; utrata 128 plastrów z testami i RLS; sprzeczne z ADR-0002 |
| Klon Qargo 1:1 | Qargo = road-first bez PL-compliance (KSeF/SENT/biała lista) i bez control tower; kopiowalibśmy cudzy sufit |
| Konfigurowalność w stylu SPEED (T-SQL per wdrożenie) | każde wdrożenie staje się dialektem nie do utrzymania — wprost ostrzega instrukcja producenta |
| Budowa 200 modułów wg katalogu bez warstwy wykonawczej | zlecenie bez stop/trip/zasobów nie domyka jobu operacyjnego spedytora |

## Źródła

Digesty z URL-ami: `docs/_source/benchmark/` (qargo-news, qargo-cases, interlan-cases-ispeed, speed-dossier, chatgpt-pdf-digest-1/2/3). Kluczowe pierwotne: api-docs.qargo.com (Concepts: Order/Consignment/Stop/Trip/Task/Resource), help.qargo.com (planning views, select&drop, expected vs actual, Qi), interlan.pl (moduły, KSeF/DPS, iSPEED), instrukcja administratora SPEED v2.5 (scribd), ogłoszenia careers.qargo.com.
