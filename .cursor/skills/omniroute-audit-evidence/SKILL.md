---
name: omniroute-audit-evidence
description: >-
  Wymaga statusu i źródła przy każdym twierdzeniu o OmniRoute (CONFIRMED,
  REQUIREMENT, TO_VERIFY, REJECTED). Używaj przy audycie, tomie wiedzy,
  cytowaniu VISION/25*, raporcie stanu kodu vs wizji, gdy user żąda
  dowodu albo zakazuje halucynacji.
---

# Dowód, nie domysł

## Status (obowiązkowy)

Każde twierdzenie o produkcie, kodzie, rynku albo liczbie ma **jeden** status:

| Status | Znaczenie |
|---|---|
| `CONFIRMED` | zdanie jest w pliku ze statusem albo jako cytat dosłowny |
| `REQUIREMENT` | kanon / plan każe to dobudować; to nie jest stan kodu |
| `TO_VERIFY` | plik sam oznacza nierozstrzygnięte albo źródło nieotwarte |
| `REJECTED` | kanon albo `AGENTS.md` tego zakazuje |

Bez statusu zdanie nie wchodzi do dokumentu.

## Źródło

Po statusie: ścieżka pliku + sekcja albo linie. Przykład: `CONFIRMED`, `docs/VISION.md` A.1.

Nie wolno: „wiadomo że”, „zazwyczaj w TMS”, „rynek pokazuje 97%”.

## Zakaz halucynacji

- Nie wymyślaj funkcji, endpointów, kolumn, vendorów, przychodu, ekstrakcji 97%, runtime silników zakazanych w `AGENTS.md`.
- Brak w przeczytanych plikach = zdanie **„w przeczytanych plikach tego nie ma”**, nie zgadywanie.
- Żądanie właściciela z czatu ≠ stan kodu. Rozdziel: cytat user vs model vs migracja.
- Liczba tylko z policzonego skanu albo z nagłówka zrzutu. Źródło daty skanu obowiązkowe.
- `Informacje z claude/vision.md` nie ładuj. Kanon = `docs/VISION.md`.
- Surowiec `D:\OMNIROUTE-badania` nie zastępuje kanonu, dopóki nie ma jawnego polecenia promocji.

## Kanon vs zrzut

| Warstwa | Plik |
|---|---|
| Kanon produktu | `docs/VISION.md` |
| Kolejka / gate | `docs/PLAN-REALIZACJA.md` |
| Rejestr M-xx | `docs/MODULES.md` |
| Audyt 2026-09-24 | `D:\OMNIROUTE-badania\25-INDEKS-AUDYTU-2026-09-24.md` i seria `25*` poza repo |

Konflikt: cytuj oba, nie „naprawiaj” w ciszy. Nie edytuj `VISION.md`, jeśli zadanie tego zabrania.

## Niekompletność audytu

Jeśli indeks mówi, że brakuje kanału — powtórz brak. Stałe luki z indeksu 2026-09-24: Supermemory niezalogowane; czaty ChatGPT/Gemini poza `25l`; dokument 1500 stron nie powstał, bo nie ma tylu faktów.
