# Kolejka — PROPOZYCJA fal T/D/P/X/F/C/V (benchmark 2026)

**To nie jest kanon.** Kanon kolejki = [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka realizacji. Wpięcie poniższych wierszy do kanonu = osobna, świadoma decyzja operatora (edycja PLAN + CURRENT poza oknem `/noc`). Do tego czasu `/noc` jedzie po kanonie (named parks), a ten plik jest materiałem decyzyjnym.

Reguły przejęte z kanonu: każda pozycja = `/plan-modul` (delta + karta pól) → `/plaster`; WIP=1; tabela+RLS przed HTTP; Auth0 (S53) przed portalami; kolizje ID żywe vs archiwum sprawdzane przy Planie pozycji (mapa kolizji w PLAN); HC bez zmian. Pozycje `TO_VERIFY` nie wchodzą do kodu bez potwierdzenia źródła (API/umowa/prawo).

## Fala T — warstwa wykonawcza (proponowana pierwsza po named parks)

| ID | Co | Zależności | Uwagi / poza zakresem |
|---|---|---|---|
| T1 | `stop` na zleceniu (typ, okno czasowe, status, lokalizacja ze słownika) | M-35, M-05 | nie mapa; nie trip; `stop_group` rozstrzyga Plan |
| T2 | `trip` + `resource` (pojazd/kierowca/naczepa; podwykonawca z `party`) | T1 | jednostka kosztowo-wykonawcza; nie telematyka; nie czas pracy |
| T3 | `container` obiekt (ISO 6346, plomby, PIN, terminale, D&D, VGM, reefer) | M-35, M-05 4.2 | karta pól gotowa; nie booking armatorski |
| T4 | Zlecenie główne / podzlecenia (`parent_shipment_id` + rodzaj relacji) | M-35 | rentowność główne+podzlecenia = widok SQL; nie druga marża |
| T5 | Task engine (szablony zadań jako dane; warunki w SQL wzorem `applies_when`) | T1–T2, M-71 | async po outboxie dopiero z konsumentem; nie LLM |
| T6 | Planning board (Timeline/Blocks/Table/Legs + mapa lazy + select&drop z walidacjami) | T1–T2 | mapa poza initial 250 kB; pre-planning; nie AIS |
| T7 | Kurs wg daty (polityka `fx_rate_basis`/offset/tabela na opłacie; domyślne w M-03) | M-23, M-08 | przeliczenie w SQL; LLM/JS nie liczą |

## Fala D — drobnica / LTL

| ID | Co | Uwagi |
|---|---|---|
| D1 | Linie + harmonogramy (cutoff, TT, dni operacyjne) | fundament sieci; nie optymalizator |
| D2 | Przesyłka/paczka ze statusami 4 poziomów + etykiety/skan | walidacja skanu wg trasy/statusu |
| D3 | Cross-dock / magazyn spedycyjny + awizacje | nie WMS pełny |
| D4 | COD + dokumenty zwrotne POD/ROD | rozliczenie pobrań w Fali F |
| D5 | Cenniki drobnicowe (strefy/waga/objętość/palety) + FSC | silnik = dane + SQL; wspólne z Falą P |
| D6 | Konsolidacje LCL własne/obce + HBL/MBL + pule numerów | łączy morze z drobnicą (wzorzec SPEED) |
| D7 | Pallet pools / saldo palet | rozliczenia sald; nie giełda palet |
| D8 | Sieci zewnętrzne pierwsza/ostatnia mila | TO_VERIFY API (Raben/Schenker/Hellmann) |

## Fala P — pricing engine

| ID | Co | Uwagi |
|---|---|---|
| P1 | Rate card warunkowy jako dane (WHEN/IF/CALC/MIN/MAX/ważność) | rozszerzenie wzorca M-18; matching w SQL |
| P2 | Charge templates (kolekcje z datami ważności bez nakładania) | wzorzec Qargo |
| P3 | Indeksacja: FSC / price index | dane + SQL |
| P4 | Local Charge Library (armator×port×serwis×typ kontenera) + wykrywanie brakujących dopłat | warning, nie fakt |
| P5 | Expected vs actual: snapshot kosztu tripa przy `in_transit` + wariancja | marża zostaje w `charge` |
| P6 | Tender quotes (ważność, limit orderów z oferty) | pogłębienie M-25/M-26/M-29 |

## Fala X — portale / mobile / API (po Auth0 S53; zastępuje ogólnik F10/S55 konkretem)

| ID | Co | Uwagi |
|---|---|---|
| X1 | Portal klienta (zlecenia, T&T, dokumenty) | Auth0 wymagane |
| X2 | Portal przewoźnika (trip, taski, upload POD, self-billing) | |
| X3 | Driver app (statusy, skan, podpis, offline) | poziom 0 telematyki (telefon = GPS) |
| X4 | Webhooki outbound + konsument outboxa (M-02) | pierwszy realny konsument zdarzeń |
| X5 | API publiczne OAuth2 (tenant/portal osobno) | OpenAPI już jest wewnętrznie |
| X6 | ePOD diff dokument vs zlecenie (zgodne/konflikt/nowe) | pogłębienie M-20; HITL zostaje |

## Fala F — finanse głębiej

| ID | Co | Uwagi |
|---|---|---|
| F1 | **KSeF live (FA(3), tryby, QR)** | priorytet — mandat PL w mocy 2026 |
| F2 | Skonto / rezerwy / rozliczenia wewnętrzne | wzorce SPEED |
| F3 | Noty księgowe + period closing | |
| F4 | Bank ISO 20022 (CAMT/MT940) + rekoncyliacja z HITL | pogłębienie M-42 |
| F5 | Delegacje / diety / wynagrodzenia kierowców | TO_VERIFY stawki per kraj |
| F6 | Windykacja + limity kredytowe w akcji (blokada zlecenia) | pogłębienie M-14/M-24 |
| F7 | Faktoring workflow (POD → weryfikacja → wypłata) | TO_VERIFY partner |
| F8 | Peppol | kalendarz UE |

## Fala C — celna / compliance

| ID | Co | Uwagi |
|---|---|---|
| C1 | SENT (zgłoszenia, GEO) | pola już na ekranach SPEED jako wzór |
| C2 | AIS-IMPORT / AES / Intrastat | TO_VERIFY dostęp PUESC |
| C3 | Biała lista / VIES / GUS live | pogłębienie M-10 lookup |
| C4 | eCMR / eFTI | cel 2027 |
| C5 | CO2 (GLEC/GHG; metodologia+wersja+źródło) | nie jedna „uniwersalna" liczba |

## Fala V — predykcje / telematyka / wieża

| ID | Co | Uwagi |
|---|---|---|
| V1 | Prediction Ledger (rekord predykcji + scorecard) | fundament wiarygodności |
| V2 | ETA planned/historical/live/risk-adjusted | po V1; metody statystyczne, nie LLM |
| V3 | D&D watchdog + rollover/ETD/ETA detekcja | morze |
| V4 | AIS wieży (leftover S32) | lazy chunk |
| V5 | Telematyka Level 0→1 (driver app → integracje GPS) | TO_VERIFY urządzenia; Level 2–3 = HZ |
| V6 | Watchtower impact chain (stock→produkcja→sprzedaż→EBITDA) + „co jeśli nie zareagujesz" | przewaga nr 1; karta wieży |
| V7 | Tachograf / czas pracy / promy art. 9 | TO_VERIFY prawo per kraj |
| V8 | What-if / scenario engine | po V6 |

## Horyzont (HZ) — decyzje biznesowe przed kodem

Booking armatorski per carrier · terminal connectors (Baltic Hub pierwszy — oficjalne API OAuth2; BCT/GCT = B2B) · promy API · giełdy market data (umowy) · chłodnie zdalne sterowanie (per urządzenie) · faktoring partner · WhatsApp · digital twins pełne · war room · autonomous negotiation (zawsze z limitami i HITL).
