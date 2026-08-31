# Dokumentacja OmniRoute

**Produkt:** OmniRoute — platforma spedycyjna
**Wydawca:** LOGMAR Sp. z o.o.
**Właściciel dokumentacji:** Sebastian Bożek

## Struktura

| Katalog | Zawartość |
|---|---|
| `00-produkt/` | wizja, persony, roadmapa |
| `01-architektura/` | przegląd, kontekst, model bezpieczeństwa |
| `02-inzynieria/` | standardy, testy, gałęzie, definicja ukończenia, obserwowalność |
| `03-operacje/` | środowiska, wdrożenia, kopie, incydenty, runbooki |
| `04-zgodnosc/` | RODO, AI Act, bezpieczeństwo |
| `05-umowy/` | regulamin, powierzenie, SLA, prywatność |
| `06-klient/` | wdrożenie, przewodniki |
| `07-projekt/` | rozstrzygnięcia, postęp, bieżące zadanie |

## Zasada utrzymania

Każdy dokument ma właściciela i datę następnego przeglądu w nagłówku.
Automatyzacja cotygodniowa raportuje dokumenty po terminie.

**Dokument bez właściciela i daty przeglądu umiera.**

## Czego tu nie ma, bo generuje się z kodu

Schemat bazy (z migracji przez `azimutt`) · dokumentacja API (z OpenAPI) ·
typy frontendu (`openapi-ts`) · changelog (`release-please`) ·
specyfikacje modułów (`docs/spec/`, kompilowane z aneksów) ·
zależności (z manifestów) · SBOM (z CI).

## Status

| Dokument | Status |
|---|---|
| Produktowe | ✓ kompletne |
| Architektura | ✓ kompletne, do uzupełnienia C4 poziom 2 i 3 |
| Inżynieria | ✓ kompletne |
| Operacje | ✓ kompletne, 9 runbooków do napisania |
| Zgodność | ✓ kompletne, wymaga weryfikacji prawnej |
| Umowy | ⚠ projekty — **wymagają kancelarii przed pierwszą umową** |
| Klient | ✓ wdrożenie, przewodniki do napisania po fazie 2 |
