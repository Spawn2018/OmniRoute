# Kolejka fal T/D/P/X/F/C/V + O — kopia robocza

**Kanon kolejki = [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka (pin operatora 2026-09-08).** Ten plik zostaje jako materiał źródłowy. `/noc` pomija named parks i jedzie od **P0**. Nie startuj nocy z tego pliku.

Fala **O** (biurko ocean) jest w PLAN, nie poniżej — karta [karty-pol-fala-o.md](karty-pol-fala-o.md).

Reguły: każda pozycja = `/plan-modul` (delta + karta pól) → `/plaster`; WIP=1; tabela+RLS przed HTTP; Auth0 (S53) przed portalami (X); kolizje ID w PLAN; HC bez zmian. Pozycje `TO_VERIFY` nie wchodzą do kodu bez potwierdzenia źródła (API/umowa/prawo).

## Natychmiastowe małe plastry (przed / równolegle z Falą T — nie czekają na wpięcie fal)

| ID | Co | Uwagi |
|---|---|---|
| M10-1 | **Dedup kontrahenta**: znormalizowany NIP / VAT-EU / EORI / DUNS unikatowy w tenancie (constraint DB + 409 z linkiem do istniejącego) + **wymóg identyfikatora biznesowego** (zakaz osób prywatnych — brak numeru = odmowa zapisu) | pogłębienie M-10; jeden plaster |
| M10-2 | Role kontrahenta jako dane (`party_role`, wiele ról na podmiocie) + forma prawna + flaga JDG + `parent_party_id` (grupy/oddziały/inny płatnik) | pogłębienie M-10; JDG → HITL w kredycie (anti-cel auto-scoringu bez zmian) |
| **B0** | Fundament bliźniaka: `prediction_ledger` + `entity_event` (append-only rama zdarzeń per obiekt) + katalog indeksów rynkowych (paliwo obok `nbp_rate`) + **`plan_snapshot`** (wersje planu: zlecenie→trip→zasób, autor, czas) + **własne TT** (rzeczywiste czasy przejazdu z actuals stopów) | **od startu** — bez logu z dnia 1 nie ma pomiaru skuteczności, pytań kontrfaktycznych ani przeplanowań „co by było gdyby"; silnik what-if przyjdzie później (V) i policzy na tych danych |

## Fala T — warstwa wykonawcza (proponowana pierwsza po named parks)

| ID | Co | Zależności | Uwagi / poza zakresem |
|---|---|---|---|
| T1 | `stop` na zleceniu (typ, okno czasowe, status, lokalizacja ze słownika) | M-35, M-05 | nie mapa; nie trip; `stop_group` rozstrzyga Plan |
| T2 | `trip` + `resource` (pojazd/kierowca/naczepa; podwykonawca z `party`) | T1 | jednostka kosztowo-wykonawcza; nie telematyka; nie czas pracy |
| T3 | `container` obiekt (ISO 6346, plomby, PIN, terminale, D&D, VGM, reefer) | M-35, M-05 4.2 | karta pól gotowa; nie booking armatorski |
| T4 | Zlecenie główne / podzlecenia (`parent_shipment_id` + rodzaj relacji) | M-35 | rentowność główne+podzlecenia = widok SQL; nie druga marża |
| T5 | Task engine (szablony zadań jako dane; warunki w SQL wzorem `applies_when`) | T1–T2, M-71 | async po outboxie dopiero z konsumentem; nie LLM |
| T6 | Planning board (Timeline/Blocks/Table/Legs + mapa lazy + select&drop z walidacjami) | T1–T2 | mapa poza initial 250 kB; podkłady z §13k; pre-planning; nie AIS |
| T7 | Kurs wg daty (polityka `fx_rate_basis`/offset/tabela na opłacie; domyślne w M-03) | M-23, M-08 | przeliczenie w SQL; LLM/JS nie liczą |

## Fala D — drobnica / LTL

| ID | Co | Uwagi |
|---|---|---|
| D1 | Linie + harmonogramy (cutoff, TT, dni operacyjne) | fundament sieci; nie optymalizator |
| D2 | Przesyłka/paczka ze statusami 4 poziomów + skan kodu | walidacja skanu wg trasy/statusu; podpięcie gdy QR Omni (§13n) |
| D3 | Cross-dock / magazyn spedycyjny + awizacje | nie WMS pełny |
| D4 | COD + dokumenty zwrotne POD/ROD | rozliczenie pobrań w Fali F |
| D5 | Cenniki drobnicowe (strefy/waga/objętość/palety) + FSC | silnik = dane + SQL; wspólne z Falą P |
| D6 | Konsolidacje LCL własne/obce + HBL/MBL + pule numerów | łączy morze z drobnicą (wzorzec SPEED) |
| D7 | Pallet pools / saldo palet | rozliczenia sald; nie giełda palet |
| D8 | Sieci zewnętrzne pierwsza/ostatnia mila + etykieta sieci po oficjalnym API | TO_VERIFY API (Raben/Schenker/Hellmann; Palletforce/Alliance jak Qargo) |
| D9 | Silnik wydruków: szablon jako dane, wymóg sieci przed wyjazdem, CMR / CMR groupage / etykieta SSCC / ZPL; skan zwrotny na `shipment_document` | U-print+PDF+Zebra; QR `shipment_ref` na każdym druku; bez kodu = HITL; §13n |

## Fala P — pricing engine

| ID | Co | Uwagi |
|---|---|---|
| **P0 leftover** | `charge.source_ref` (nullable na starych wierszach fixture; obowiązkowe na INSERT z myta/PP) | HC-05 / zasada 5; V2b i F11 tego wymagają — nie nowa fala, nie zgadywać numeru migracji |
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
| X6 | ePOD / CMR diff vs zlecenie (zgodne/konflikt/nowe) | po X9 (ramki + pewność); HITL zostaje |
| X7 | Lejek oferty: `quote_engagement` (sent / email_opened / pdf_viewed / replied / converted) + czasy w SQL; hostowany PDF z tokenem; piksel tylko po zgodzie | pogłębienie M-26/M-57/M-32/M-29; mailto bez Graph = link PDF jest sygnałem; nie PostHog |
| X8 | Podkłady map: katalog jako dane; preferencje użytkownika (darmowe on/off); sekrety płatnych u admina tenanta (HC-05) + instrukcja w UI | [podklady-map-admin.md](podklady-map-admin.md); nie tile.openstreetmap.org |
| X9 | Silnik zdjęcia (ML Kit / VisionKit) + enhance „skaner płaski” (OpenCV: kadr, cień, biel papieru, ~300 DPI) + bbox/pewność + split | wygląd skanera, nie GAN; FV bez wymazywania plam; §13o |

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
| F9 | `purchase_invoice` + adapter ERP: Omni wystawia przychodowe; do FK FS + FZ | KSeF tylko Omni; [erp-fk-adapter.md](erp-fk-adapter.md) |
| F10 | Ingest FV kosztowych: mail / KSeF Subject2 / skan → `extraction_draft` → ranking zleceń (SQL) → HITL accept; `shipment_ref` na zleceniach wychodzących | wzór M-20; XML FA(3) bez LLM; nie auto-link; §13m |
| F11 | Cyfrowa książka nadawcza: `paper_post` na FV → `postal_dispatch` + EN + śledzenie + EPO | papier ≠ wyłączenie KSeF; bez nadania nie ma „wysłana”; §13p |

## Fala C — celna / compliance

| ID | Co | Uwagi |
|---|---|---|
| C1 | SENT + SENT-GEO (PUESC) | wzór pól ze SPEED; flaga na T6 |
| C2 | AIS-IMPORT / AES / Intrastat | TO_VERIFY dostęp PUESC |
| C3 | Biała lista / VIES / GUS live | pogłębienie M-10 lookup |
| C4 | eCMR / eFTI | cel 2027; interop DIWASS |
| C5 | CO2 (GLEC/GHG; metodologia+wersja+źródło) | nie jedna „uniwersalna" liczba |
| C6 | Odpady: BDO/KPO kraj + DIWASS/WSR transgranica | oficjalne API MOS + KE; zmiana BDO API 1.01.2027 |
| C7 | Katalog `monitoring_scheme` (EKAER, BIREG, RO e-Transport, EMCS, NCTS, Trackdéchets, RENTRI…) | tylko potwierdzone systemy; brak klona ≠ wymysł |
| C8 | `party_document` + blokada `POST shipment` (polisa / składka / licencja); odblokowanie nowym dokumentem | po T2; HITL extract; nie scoring osoby |
| C9 | Snapshot Trans.eu: `overall_rating`, satisfaction, TransRisk, `documents.expire_date` | zakaz scrapingu; brak publicznego API komentarzy słownych; [ ] TO_VERIFY `api@trans.eu`; próg blokady = M-03 |

## Fala V — predykcje / telematyka / wieża

| ID | Co | Uwagi |
|---|---|---|
| V1 | Prediction Ledger (rekord predykcji + scorecard) | fundament wiarygodności |
| V2 | ETA planned/historical/live/risk-adjusted + pogoda Open-Meteo **wzdłuż trasy w całej Europie** | po V1; metody statystyczne, nie LLM |
| V2b | Toll engine EU/EFTA: klasa/osie/emisja/CO₂/data; winieta osobno; `charge` z `source_ref` | PTV/NAPSPAN/TollCalc albo taryfy publiczne; brak taryfy = warning, nie zmyślona kwota |
| V3 | D&D watchdog + rollover/ETD/ETA detekcja | morze |
| V4 | AIS wieży (leftover S32) | lazy chunk |
| V5 | Omni Telematics Hub: `PositionEvent` + adaptery L0 / L1a (Teltonika+Queclink = `omni_telematic`) / **P0: GBOX, IKOL, Flotis, Wialon** / L1b / L1c | `omni_telematic` + umowa = poll floty. `external_api` = 3 **dni robocze** bez trip, potem stop; nowy trip włącza. Zero własnego HW. Sekrety HC-05 |
| V5b | Widoczność giełd per transport (Trans.eu monitoring/trace, TIMOCOM Tracking, Transporeon Open Visibility) + `exchange_message` tylko gdy tenant jest stroną + `quoted_amount` na `carrier_inquiry` + metryki jobu spedytora | zakaz scrapingu czatów; Teleroute = oferty, nie GPS |
| V6 | Watchtower impact chain (stock→produkcja→sprzedaż→EBITDA) + „co jeśli nie zareagujesz" | przewaga nr 1; karta wieży |
| V7 | Tachograf / czas pracy / promy art. 9 | TO_VERIFY prawo per kraj |
| V8 | What-if / scenario engine | po V6 |

## Horyzont (HZ) — decyzje biznesowe przed kodem

Booking armatorski per carrier · terminal connectors (Baltic Hub pierwszy — oficjalne API OAuth2; BCT/GCT = B2B) · promy API · giełdy market data (umowy) · chłodnie zdalne sterowanie (per urządzenie) · faktoring partner · WhatsApp · digital twins pełne (Network Twin) · war room · autonomous negotiation (zawsze z limitami i HITL) · procurement autopilot · contract intelligence · regulatory radar · multi-objective optimizer · memory graph · executive AI · IT support agent · slot intelligence/secure chain/port identity · Omni Market Intelligence (osobny produkt) · kolejne native adaptery GPS poza P0 (reszta listy PL/EU po umowie i dokumentacji; P0 = GBOX/IKOL/Flotis/Wialon w V5) · energy intelligence · Connected Carrier / finansowanie GPS (bez własnego HW) · Transformation Office · bliźniak urzędu · P&O Freight API.

Silniki + luki PDF: [benchmark-tms-2026.md](benchmark-tms-2026.md) §12 i §13j. Audyt źródeł: [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md).
