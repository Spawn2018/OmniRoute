# Benchmark TMS 2026: Qargo + interLAN SPEED + wizja OmniRoute — matryca unii funkcjonalności

**Data:** 2026-09-07 · **Decyzja:** [ADR-0004](../adr/0004-benchmark-qargo-speed-2026.md) · **Kolejka:** [kolejka-propozycja.md](kolejka-propozycja.md) (propozycja, nie kanon) · **Pola:** [karty-pol-fala-t.md](karty-pol-fala-t.md)  
**Surowe digesty źródłowe (nie ładować hurtowo):** `docs/_source/benchmark/`

Trzy źródła: **MC** = master-context + PDF rozmowy (376 stron, wizja OmniRoute), **Q** = Qargo (zweryfikowane: API docs, Knowledge Hub, 59 newsów, 44 case'y), **S** = interLAN SPEED (dossier 37 źródeł, zrzuty ekranów, wdrożenia).  
Status: **DONE** (w kodzie, M-xx) · **CZĘŚĆ** · **PARK** (named park) · **BRAK**.  
Werdykt: **JEST** (nic nie robić) · **KOPIUJ** (adoptować koncepcję) · **ULEPSZ** (adoptować + przewaga) · **POMIŃ** (świadomie nie).  
Fala: **0** (w kodzie) · **T** wykonawcza · **D** drobnica · **P** pricing · **X** portale/mobile · **F** finanse · **C** celna · **V** predykcje/telematyka/wieża · **HZ** horyzont (decyzja biznesowa / TO_VERIFY).

## Wnioski z badań (skrót)

- Oś oczekiwań klientów TMS (59 newsów + 44 case'y Qargo): **likwidacja przepisywania danych**, cash flow, ePOD, puste kilometry (31% UK / 25,9% UE). Najlepiej sprzedają: AI order entry (−75% adminu), fakturowanie z integracjami FK, driver app. Braki rynku: e-CMR, WhatsApp, AI-planowanie.
- Kalendarz regulacyjny: Peppol BE I 2026 · Francja CTC IX 2026/2027 · **KSeF PL — mandat już w mocy 2026** · eCMR/eFTI cel 2027 · NIS2 · CSRD (po Omnibus I) · myto NL VII 2026. Pakiet Mobilności i AI Act nieobecne w komunikacji Qargo — wolna przestrzeń.
- interLAN: wdrożenia z bólem (ROHLIG SUUS ~rok poślizgu; Rhenus „łzy i zgrzytanie zębami"), konfiguracja = custom dev T-SQL, brak publicznego API i cennika; iSPEED (XI 2025) młody. Wniosek: przewagę buduje czas-do-wartości i konfiguracja jako dane.
- Qargo nie adresuje załadowców/control tower (tylko przewoźnik/spedycja/3PL) — wieża z łańcuchem skutków pozostaje wolną pozycją.
- PDF: pełne listy pól 43 obiektów modelu wspólnego + 8 digital twinów (digesty 1–3); rekomendacja strategiczna rozmowy: jeden silnik OmniRoute, dwie perspektywy (Operator OS + Enterprise), wejście przez Watchtower. Obiecany blueprint końcowy nigdy nie powstał (awaria generowania) — domyka go ta matryca.

## 1. Rdzeń oferty i wyceny

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| RFQ z maila (inbound → RFQ → wycena) | MC/Q/S | DONE M-32/M-28/M-21 | JEST | 0 |
| Ekstrakcja cenników/dokumentów z HITL | MC/Q | DONE M-20 | JEST | 0 |
| Silnik wyceny SQL (INSERT…SELECT) | MC | DONE M-21 | JEST | 0 |
| Stawki niemutowalne + `source_ref` | MC | DONE M-07 | JEST | 0 |
| `charge` buy+sell = marża | MC/S | DONE M-08 | JEST | 0 |
| Katalog kodów opłat + aliasy | S/Q | DONE M-06 | JEST | 0 |
| Kursy NBP tabela A | S/MC | DONE M-23 | JEST | 0 |
| Dopłaty warunkowe (`applies_when` w SQL) | S/Q | DONE M-18 | ULEPSZ (rozszerzyć na rate cards) | P |
| Dokument oferty + numeracja z szablonu | S | DONE M-26/M-03 | JEST | 0 |
| Wycena wsadowa | MC | DONE M-27 | JEST | 0 |
| Akceptacja oferty won/lost przez szynę decyzji | Q | DONE M-29/M-71 | JEST | 0 |
| Zapytania buy-side do przewoźników | Q/S | DONE M-30 | JEST | 0 |
| Porównanie odpowiedzi + spread w `charge` | Q | DONE M-31 | JEST | 0 |
| Tender quotes (statusy, ważność, limit orderów z oferty) | Q | CZĘŚĆ (M-25/M-26/M-29) | ULEPSZ | P |
| Kanały armatorskie live HTTP | MC | PARK S21 (brak umowy) | KOPIUJ przy umowie | HZ |

## 2. Warstwa wykonawcza (największa luka — definiuje job floty z S50)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| `stop` / `stop_group`: punkt operacyjny z oknem czasowym, typem (ZA/WY/cło/prom/terminal), statusem | Q/S | BRAK (leg = relacja, nie punkt) | KOPIUJ | T1 |
| `trip`: jednostka wykonawczo-kosztowa; stopy z wielu `shipment` | Q | BRAK | KOPIUJ | T2 |
| `resource`: pojazd / kierowca / naczepa (+ dokumenty i ważności) | Q/S/MC | PARK S50 | KOPIUJ | T2 |
| Podwykonawca na tripie (subcontractor) | Q/S | CZĘŚĆ (`party`) | ULEPSZ | T2 |
| Kontener jako obiekt (plomby, PIN, terminale, VGM, D&D) | S/MC | BRAK | KOPIUJ | T3 |
| Zlecenie główne / podzlecenia (wynik spływa na główne) | S | BRAK | KOPIUJ | T4 |
| Task engine: warunki (trasa/towar/serwis/klient) → zadania | Q/MC | BRAK | ULEPSZ (reguły = dane; async po outboxie gdy konsument) | T5 |
| Planning board: Timeline / Blocks / Table / Legs | Q | BRAK | KOPIUJ | T6 |
| Mapa planistyczna: selekcja prostokąt/polygon, do 1000 orders, markery typ+status | Q | BRAK | KOPIUJ (lazy chunk, nie initial 250 kB) | T6 |
| Select & Drop multi-order na zasób | Q | BRAK | ULEPSZ (+walidacje: ładowność, ADR, okna, czas pracy, marża) | T6 |
| Pre-planning (przestrzeń robocza przed przypisaniem) | Q | BRAK | KOPIUJ | T6 |
| Auto-assign resources (reguły przypisań) | Q | BRAK | KOPIUJ | T7 |
| Dyspozytor: restrykcje dokumentów/czasu pracy przy planowaniu | S/MC | BRAK | ULEPSZ | T7/V |
| Expected vs actual cost (snapshot kosztu przy przejściu w in-transit) | Q/S | CZĘŚĆ (M-08 kalkulacja + M-41 faktury na wycenie) | ULEPSZ (snapshot na tripie) | P |
| Kurs wg daty (tabela wg ETD / daty załadunku / −1 dzień roboczy) | S | BRAK | KOPIUJ (spójne z NBP D-1, art. 31a VAT) | T7 |
| Plan vs wykonanie (jakość planowania) | S | BRAK | KOPIUJ | V |

## 3. Drobnica / LTL (siła SPEED)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Linie + harmonogramy (cutoff, transit time, dni operacyjne) | S/MC | BRAK | KOPIUJ | D |
| Cross-dock / magazyn spedycyjny | S/MC | BRAK | KOPIUJ | D |
| Statusy 4 poziomów: przesyłka / paczka / punkt / trasa | S | BRAK | KOPIUJ | D |
| Etykiety + skanowanie kodów (walidacja wg trasy/statusu) | S/MC/Q | BRAK | KOPIUJ | D |
| Awizacje | S | BRAK | KOPIUJ | D |
| COD (pobrania) + dokumenty zwrotne POD/ROD | S | BRAK | KOPIUJ | D |
| Cenniki drobnicowe (strefy, waga, objętość, palety) + FSC | S/MC | BRAK | KOPIUJ | D/P |
| Sieci zewnętrzne pierwsza/ostatnia mila (Raben/Schenker/Hellmann) | MC | BRAK | KOPIUJ (API TO_VERIFY) | D/HZ |
| Pallet pools / saldo palet + rozliczenia | Q/MC | BRAK | KOPIUJ | D |
| Dystrybucja: podział FV kosztowej algorytmem do sztuki indeksu | S | BRAK | ULEPSZ | D/F |

## 4. Pricing engine

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Rate cards warunkowe (WHEN/IF/CALCULATE/MIN/MAX/waluta/ważność) jako dane | Q/MC | CZĘŚĆ (wzorzec M-18) | ULEPSZ | P |
| Charge templates (reużywalne kolekcje z datami ważności) | Q | BRAK | KOPIUJ | P |
| Indeksacja (fuel surcharge, price index) | Q | BRAK | KOPIUJ | P |
| Local Charge Library (armator × port × serwis × typ kontenera) | MC | BRAK | KOPIUJ | P |
| Wykrywanie brakujących dopłat w ofercie (warning, nie fakt) | MC | BRAK | KOPIUJ | P |
| Oferta morska = 14 typów opłat (fracht + dopłaty + port + cło + trucking) | MC/S | CZĘŚĆ (`charge_code`) | ULEPSZ | P |
| Market data giełd (Transporeon Insights, Trans.eu accepted price) | MC | BRAK | KOPIUJ (umowy TO_VERIFY) | HZ |
| Benchmark stawek własnych (historia `rate_line`) | MC | CZĘŚĆ (dane są) | ULEPSZ | V |

## 5. Morze / intermodal / kolej

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Nogi FCL/LCL/rail/china_rail na zleceniu | S/MC | DONE M-48–M-51 | JEST | 0 |
| Routing portów POL/POD/WY z datami plan/rzecz. | S | CZĘŚĆ (legs + `port`) | ULEPSZ (stopy z datami) | T1 |
| HBL/MBL + pule numerów master | S | BRAK | KOPIUJ | D |
| VGM (miejsce, waga, cut-off) | S | BRAK | KOPIUJ | T3 |
| Demurrage / detention watchdog + free time | MC/S | BRAK | KOPIUJ | V |
| Rollover / zmiana ETD/ETA/vessel — detekcja + alert | MC | BRAK | KOPIUJ | V |
| AIS vessel tracking | MC | PARK (leftover wieży) | KOPIUJ | V |
| Konsolidacje LCL własne/obce + dekonsolidacja | S | BRAK | KOPIUJ | D |
| Booking armatorski | MC | BRAK | KOPIUJ (per carrier TO_VERIFY) | HZ |
| Intermodal: rozkłady połączeń, bulk move między odjazdami | Q | CZĘŚĆ (M-49/M-50 nogi) | ULEPSZ | D |
| Terminal connector (SDK 14 funkcji; Baltic Hub OAuth2 pierwszy; BCT/GCT B2B; audyt P0–P2 w digestach) | MC | BRAK | KOPIUJ | HZ |
| Promy: wyszukiwanie / booking / cutoff / wpływ na czas pracy | MC/S | BRAK | KOPIUJ (API operatorów TO_VERIFY) | HZ |

## 6. Portale / mobile / API

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Portal klienta (zlecenia, T&T, dokumenty) | Q/S/MC | PARK F10 (po Auth0 S53) | KOPIUJ | X |
| Portal przewoźnika / podwykonawcy | Q/S/MC | PARK F10 | KOPIUJ | X |
| Driver app (statusy, skan POD, podpis, geofencing, offline) | Q/S/MC | BRAK | KOPIUJ | X |
| Self-billing przewoźnika | S | BRAK | KOPIUJ | X/F |
| ePOD + diff dokument vs zlecenie (zielony/konflikt/nowa wartość) | Q | CZĘŚĆ (M-20 HITL) | ULEPSZ | X/P |
| Giełda zleceń dla przewoźników partnerskich | S | BRAK | KOPIUJ | HZ |
| Webhooki outbound (visibility / fleet / accounting) | Q/MC | CZĘŚĆ (M-02 outbox, brak konsumenta) | ULEPSZ | X |
| API publiczne OAuth2 + osobne API tenant/portal | Q | CZĘŚĆ (OpenAPI wewnętrzne) | KOPIUJ | X |
| WhatsApp / komunikatory | Q | BRAK | POMIŃ teraz | HZ |
| Bilety promowe w portalu | S | BRAK | KOPIUJ | HZ |

## 7. Finanse

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Faktura sprzedaży na zleceniu | S/Q | DONE M-40 | JEST | 0 |
| KSeF live (FA(3), tryby online/offline, QR) | S/MC | CZĘŚĆ (`ksef_ref`) | KOPIUJ — priorytet (mandat 2026) | F |
| Rozliczenie wyceny z fakturą | S | DONE M-41 | JEST | 0 |
| Bank + płatności | MC | DONE M-42 | ULEPSZ (ISO 20022 CAMT/MT940, rekoncyliacja z HITL) | F |
| Koszt pieniądza / FX / przepływy / CTS / dekrety / zbiorcze FV | MC | DONE M-43–M-47, M-91 | JEST | 0 |
| Faktoring (POD → weryfikacja → przyspieszona wypłata) | MC | BRAK | KOPIUJ (partner TO_VERIFY) | F/HZ |
| Skonto / rezerwy / rozliczenia wewnętrzne między lokalizacjami | S | BRAK | KOPIUJ | F |
| Delegacje / diety / wynagrodzenia kierowców | S/MC | BRAK | KOPIUJ | F/HZ |
| Windykacja + limity kredytowe w akcji (blokada przyjęcia zlecenia) | S/MC | CZĘŚĆ (M-14/M-24) | ULEPSZ | F |
| Peppol e-invoicing | Q | BRAK | KOPIUJ | F |
| Period closing (zamykanie okresów) | Q | BRAK | KOPIUJ | F |
| Noty księgowe | S | BRAK | KOPIUJ | F |
| Rentowność wielowymiarowa (zlecenie/spedytor/pojazd/klient/trasa) | S | CZĘŚĆ (M-15 tablica) | ULEPSZ | F/V |

## 8. Celna / compliance

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| SENT (zgłoszenia, nr ref, GEO lokalizator) | S/MC | BRAK | KOPIUJ | C |
| AIS-IMPORT / AES / ZEFIR / OSOZ2 / PUESC | S/MC | BRAK | KOPIUJ (dostęp TO_VERIFY) | C |
| Intrastat | S | BRAK | KOPIUJ | C |
| Sankcje screening na kontrahencie | MC | DONE M-53 | ULEPSZ (statki/ładunki/trasy) | C/V |
| Biała lista / VIES / GUS lookup | MC | CZĘŚĆ (M-10 fixture) | ULEPSZ | C/F |
| eCMR / eFTI | Q/MC | BRAK | KOPIUJ (cel 2027) | C |
| RODO (access/erasure + tombstone) | MC | DONE M-56 | JEST | 0 |
| ADR advisor (drogowe ≠ morskie ≠ kolejowe; tunele, klasy) | MC | CZĘŚĆ (M-52 katalog UN) | ULEPSZ | V/HZ |
| CO2 / CBAM (GLEC/GHG, metodologia + wersja + źródło) | Q/MC | BRAK | KOPIUJ | V |
| AI Act: minimal risk, Art. 50 label, zakaz scoringu osób | MC | DONE (praktyki w kodzie) | JEST | 0 |

## 9. Predykcje / telematyka / wieża (oś przewagi)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| ETA: planned / historical / live / risk-adjusted | MC | BRAK | KOPIUJ | V |
| Prediction Ledger (rekord predykcji, scorecard, kalibracja) | MC | BRAK | KOPIUJ | V |
| Champion/challenger + drift detection | MC | BRAK | KOPIUJ | V |
| Telematyka Level 0–3 (driver app → integracje GPS → ZSL/SENT → własny HW) | MC | BRAK | KOPIUJ (urządzenia TO_VERIFY) | V/HZ |
| Tachograf / czas pracy / Pakiet Mobilności / promy art. 9 561/2006 | S/MC | BRAK | KOPIUJ | V/HZ |
| Chłodnie: temperatura, alarmy, zdalne sterowanie | MC | BRAK | KOPIUJ (per urządzenie TO_VERIFY) | HZ |
| Watchtower: łańcuch skutków shipment → stock → produkcja → sprzedaż → EBITDA; „co jeśli nie zareagujesz" | MC | CZĘŚĆ (S32 liczniki) | ULEPSZ — przewaga nr 1 | V |
| What-if / scenario engine (port zamknięty, paliwo, bankructwo przewoźnika) | MC | BRAK | KOPIUJ | V/HZ |
| War room zakłóceń (7–10 kroków reakcji) | MC | BRAK | KOPIUJ | HZ |
| Digital twins (pojazd, kierowca, kontener, terminal, sieć) | MC | BRAK | KOPIUJ | V/HZ |
| Pogoda / profil wysokości / predykcja spalania | MC | BRAK | KOPIUJ | V/HZ |
| Toll engine (klasa, osie, emisja, kraj, odcinek) | S/MC | BRAK | KOPIUJ | V/HZ |
| Scoring przewoźnika / plan vs wykonanie KPI | S/Q | CZĘŚĆ (M-13) | ULEPSZ | V |

## 10. AI

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Email → RFQ/wycena (klasyfikacja, ekstrakcja, dopasowanie kontrahenta) | Q/MC | DONE fundament | ULEPSZ (draft zlecenia z maila) | T4/X |
| Document Intelligence diff (CMR/POD vs zlecenie: zgodne/konflikt/nowe) | Q | CZĘŚĆ (M-20/M-69) | ULEPSZ | P/X |
| AI summaries wątków mailowych | Q | BRAK | KOPIUJ (Art. 50 label) | HZ |
| Chat-based validation rules (opis słowami → reguła jako dane → test na próbie → aktywacja) | Q/MC | BRAK | ULEPSZ | HZ |
| AI chat agent (pytania o rekordy i system) | Q | CZĘŚĆ (M-57 copilot) | ULEPSZ | HZ |
| Carrier procurement agent (RFQ → odpowiedzi → ranking) | MC | CZĘŚĆ (M-30/M-31 ślad) | ULEPSZ | HZ |
| CFO narracja po SQL (LLM nie liczy) | MC | DONE M-15/S57 | JEST | 0 |
| Zasada: LLM orkiestruje, silniki liczą | MC | DONE (HC-02) | JEST | 0 |

## 11. Platforma

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Saved views (kolumny, filtry) + gęstość compact | Q | DONE (`table_view`, DataTableShell) | JEST | 0 |
| Współdzielenie widoków (prywatny / zespół / organizacja) | Q | CZĘŚĆ (widok per user) | ULEPSZ | X |
| Konfiguracja jako dane (anty-wzorzec SPEED: T-SQL per wdrożenie) | S/MC | DONE M-03 | JEST — lepszy mechanizm | 0 |
| Słowniki per tenant + teksty ustaleń + szablony | S | CZĘŚĆ | ULEPSZ | T7/D |
| Szablony dokumentów / wydruki (B/L, FV, zlecenie) | S/MC | CZĘŚĆ (U-print ID) | ULEPSZ | F |
| Numeracja per lokalizacja / oddział / dział | S | CZĘŚĆ (M-03 prefiks/szablon) | ULEPSZ | F |
| Multi-tenant RLS + OpenFGA | MC | DONE HC-01 | JEST — przewaga nad oboma | 0 |
| Audit trail decyzji (Decision Ledger) | MC | CZĘŚĆ (M-71 + HITL) | ULEPSZ | V |
| Obserwowalność / OTel | MC | PARK S59 | — | park |

## 12. Silniki enterprise / C-level (komplet z PDF rozmowy — nic nie ginie)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Digital twin „do wszystkiego" (pojazd, kierowca, kontener, terminal, statek, magazyn, proces, pracownik, klient) | MC | BRAK jako warstwa; dane cząstkowe już w modułach | KOPIUJ dwuetapowo: **B0 od startu** = rejestr zdarzeń + prediction_ledger + indeksy rynkowe (bez logu z dnia 1 nie ma czego symulować); pełne twiny i symulacje = warstwa na zebranych danych | **B0 → V/HZ** |
| Omni Network Digital Twin (replika całej sieci: dostawcy → klienci) | MC | BRAK | KOPIUJ | HZ |
| Business Impact Graph (shipment → inventory → SKU → linia produkcyjna → zamówienie → revenue → margin → cash) | MC | BRAK | KOPIUJ — rdzeń wieży (V6) | V |
| Revenue at Risk + Working Capital Engine (DSO, cash flow ryzyka) | MC | BRAK | KOPIUJ | V/HZ |
| What-if / Scenario Engine (paliwo, zamknięcie portu, bankructwo przewoźnika) | MC | BRAK | KOPIUJ | V |
| Disruption War Room (7–10 kroków reakcji) | MC | BRAK | KOPIUJ | HZ |
| Procurement Autopilot (potrzeba → RFQ → negocjacje → award z akceptacją człowieka) | MC | CZĘŚĆ (M-30/M-31 ślad zapytań i porównań) | ULEPSZ | HZ |
| Contract Intelligence (FV przewoźnika vs umowa — wykrycie rozbieżności; kary/terminy jako reguły operacyjne) | MC | BRAK | KOPIUJ | HZ |
| Regulatory Radar (monitor zmian przepisów UE/krajowych) | MC | BRAK | KOPIUJ | C/HZ |
| Counterparty Risk Engine (bankructwo, opóźnienia płatnicze, compliance — podmiot, nigdy osoba fizyczna) | MC | CZĘŚĆ (M-13 karta, M-14 kredyt, M-54 fraud flag) | ULEPSZ | V/HZ |
| Fraud & Anomaly Engine (anomalia ≠ dowód — zawsze flaga do recenzji) | MC | CZĘŚĆ (M-54) | ULEPSZ | HZ |
| Multi-Objective Optimizer (koszt × czas × ryzyko × CO2 × zgodność wg preferencji klienta) | MC | BRAK | KOPIUJ | HZ |
| Autonomous Negotiation Engine (negocjacje w zadanych limitach ceny/marży) | MC | BRAK | KOPIUJ ostrożnie — zawsze limity + HITL | HZ |
| Memory Graph (encje + zdarzenia + decyzje; „co zadziałało w podobnej sytuacji") | MC | BRAK | KOPIUJ | HZ |
| Decision Ledger (rekomendacja → dowody → decyzja → człowiek → wynik; metryki trafności AI) | MC | CZĘŚĆ (M-71 szyna decyzji + HITL) | ULEPSZ | V |
| Executive AI / early warning dla zarządu (pytania o straty, nierentowne trasy, ryzyko) | MC | BRAK | KOPIUJ | HZ |
| Energy Intelligence (flota EV, energia magazynów) | MC | BRAK | POMIŃ teraz | HZ |
| Customer Chat (status/ETA/dokumenty/reklamacje) — wg ustaleń MC §63: status widać w portalu OD RĘKI, chat nie jest do tego | MC/Q | BRAK | KOPIUJ z podziałem ról | X/HZ |
| IT Support Agent (ticket → analiza → propozycja naprawy → człowiek zatwierdza) | MC | BRAK | KOPIUJ | HZ |
| Email Digital Twin spedytora (czyta pocztę → draft → akceptacja → wysyłka z jego skrzynki) | MC | CZĘŚĆ (M-57 `mail_draft` + S18 świadoma wysyłka) | ULEPSZ | X |
| Slot Intelligence + Secure Chain + Port Identity (predykcja slotu, custody kontenera, sejf poświadczeń portowych) | MC | BRAK | KOPIUJ | HZ (po konektorach terminali) |
| Omni Market Intelligence (produkt danych: stawki, capacity, prognozy, benchmarki) | MC | BRAK | KOPIUJ — osobna linia produktowa | HZ |
| Telematyka jako biznes (5 modeli finansowania GPS, Connected Carrier program, hardware SaaS) | MC | BRAK | decyzja biznesowa | HZ |
| Generator raportów (KPI, rentowność, predykcje) — LLM pisze narrację po SQL, nigdy nie liczy | MC | CZĘŚĆ (M-15 narracja `/finance`) | ULEPSZ | F/V |
| Widoki per rola: spedytor FTL (A→B) ≠ dyspozytor drobnicy (sieć/linie/wypełnienie) ≠ morze (kontenery/cut-offy) | S/Q | CZĘŚĆ (saved views + DataTableShell) | ULEPSZ — osobne boardy na wspólnym modelu stop/trip/resource | T6/D |

## 13. Uzupełnienie po ponownym przeglądzie katalogu §92 + wymagania operatora (2026-09-07 wieczór)

### 13a. Kontrahent (pogłębienie M-10 — wymagania operatora)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| **Dedup kontrahenta**: unikat w tenancie po znormalizowanym NIP / VAT-EU / EORI / DUNS; przy próbie duplikatu 409 + link do istniejącego | operator | BRAK (jest `resolve` po tax_id, brak constraintu) | KOPIUJ | **natychmiastowy mały plaster** |
| **Zakaz osób prywatnych**: rekord kontrahenta wymaga identyfikatora biznesowego (NIP/VAT-EU/EORI/nr rejestrowy kraju) — brak = odmowa zapisu | operator | BRAK | KOPIUJ | ten sam plaster co dedup |
| **Role kontrahenta** (wiele na jednym podmiocie, wzór Qargo „Company = customer i subcontractor"): zleceniodawca · przewoźnik drogowy · armator · agent morski · coloader · spedytor partnerski (sieć) · terminal/port · magazyn/skład celny · agencja celna · ubezpieczyciel · faktor · dostawca paliwa/kart · wywiadownia · dostawca telematyki | operator/Q/S | CZĘŚĆ (`party` + `carrier_profile`) | ULEPSZ — role jako dane (tabela `party_role`), nie enum na sztywno | M-10 pogłębienie |
| **Forma prawna + flaga JDG** (osoba fizyczna prowadząca działalność — inny reżim RODO/AI Act) | operator/prawo | BRAK | KOPIUJ | M-10 pogłębienie |
| Grupy kapitałowe / oddziały / „inny płatnik" (`parent_party_id`) | S | BRAK | KOPIUJ | M-10 pogłębienie |
| Segmentacja handlowa (klasa A/B/C wg obrotu/marży — licz SQL, nie ręcznie; branża; kierunki) | propozycja | BRAK | KOPIUJ | F/V |
| Wywiadownie gospodarcze (KRD / Coface / D&B / CreditSafe) — konektory; raport jako załącznik recenzji kredytowej; **JDG tylko HITL, nigdy auto-scoring** | operator/MC | CZĘŚĆ (M-14 88.0 `bureau_attachment_ref` — wskazanie raportu już jest) | ULEPSZ | F6 + HZ (umowy z wywiadowniami) · prawo: karta `_knowledge/market/005` |

### 13b. Fundament cyfrowego bliźniaka — OD STARTU (wymaganie operatora)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| `prediction_ledger` — każda predykcja zapisana z wejściem/pewnością/wersją modelu → potem actual + błąd | MC | BRAK | KOPIUJ | **B0 (przed/równolegle z Falą T)** |
| `entity_event` — append-only rejestr zachowań per obiekt (pracownik, klient, przewoźnik, agent, armator): kto/co/kiedy/kontekst | MC | CZĘŚĆ (tracking M-36, decyzje M-71, outbox M-02 — brak wspólnej ramy) | ULEPSZ — jedna rama zdarzeń | **B0** |
| Katalog indeksów rynkowych (paliwo, frachty — obok `nbp_rate`): data + wartość + źródło | MC | CZĘŚĆ (M-23 kursy) | KOPIUJ — bez historii indeksów nie ma pytań „co by było gdyby paliwo nie podrożało" | **B0** |
| Kontrfaktyczne „what-if" na zebranych danych (marża klienta X przy innym paliwie/kursie) | MC | BRAK | KOPIUJ — silnik przychodzi później (V), ale liczy na danych logowanych od B0 | V |

### 13c. Reszta katalogu §92 (domknięcie inwentarza)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| CRM (lead → szansa → oferta; aktywności handlowe) | MC | BRAK (`party` to katalog, nie lejek) | KOPIUJ | X/HZ |
| Spedycja lotnicza (AIR OS: HAWB/MAWB, pule numerów master, e-rates) | MC/S | BRAK | KOPIUJ | HZ (osobna fala wzorem nóg morskich) |
| Floating trailers (naczepa bez ciągnika na promie; kierowcy A/B) | MC | BRAK | KOPIUJ — model `resource` z naczepą jako osobnym zasobem to umożliwia | T2 (scenariusz w Planie) |
| Multi-manning (dwóch kierowców; art. 8–9 rozp. 561/2006, prom ≠ zwykły postój) | MC | BRAK | KOPIUJ | V7 |
| Diagnostyka pojazdu (kody błędów, predictive maintenance) | MC | BRAK | KOPIUJ | HZ (telematyka L1+) |
| Huckepack / wagony kieszeniowe | MC | CZĘŚĆ (M-49 nogi rail) | ULEPSZ | D |
| Magazyn celny + miejsce uznane | MC | BRAK | KOPIUJ | C |
| WMS pełny (inventory, przyjęcia/wydania, lokacje) | MC | BRAK | KOPIUJ | HZ (katalog 71–212 „WMS") |
| Traffic live + historyczny (profil dnia/godziny/sezonu) jako dane ETA | MC | BRAK | KOPIUJ | V |
| Restrykcje drogowe / green zones / LEZ / toll engine (dane map + naliczenia) | MC/Q/S | BRAK | KOPIUJ | V/HZ (źródła danych do wyboru: darmowe → płatne po rachunku kosztów) |
| Karty paliwowe + zbiorniki paliwa (tankowania, wydania, anomalie) | MC/S | BRAK | KOPIUJ | F/HZ |
| Klasyfikacja stawek spot vs contract + historia rynkowa | MC | CZĘŚĆ (`rate_line` ma źródło i czas) | ULEPSZ | P |
| Tender management / Tender AI (analiza dokumentacji przetargowej, matryca odpowiedzi, rentowność; reprezentacja klienta korporacyjnego = 4PL) | MC | BRAK | KOPIUJ | HZ |
| Contract management (umowy, SLA → łączy się z Contract Intelligence §12) | MC | BRAK | KOPIUJ | HZ |
| Financial controlling (budżety, rezerwy okresowe — ponad tablicę M-15) | MC | CZĘŚĆ | ULEPSZ | F |
| Workflow engine / custom workloads admina (procesy definiowane przez użytkownika) | MC | CZĘŚĆ (task engine T5 = fundament) | ULEPSZ | T5 → HZ |
| Incident management (awarie operacyjne ≠ wyjątki zleceń M-37) | MC | CZĘŚĆ (M-37) | ULEPSZ | V |
| Import zleceń obcych spedycji (OCR druku obcego → zlecenie + analiza warunków/ryzyk) | MC | CZĘŚĆ (M-20 ekstrakcja HITL) | ULEPSZ | X |
| Pogoda / profil wysokości / spalanie — potwierdzenie: już w § 9 (V) | MC | — | — | V |
| Palety saldo — potwierdzenie: już w § 3 (D7) | MC | — | — | D |

### 13d. Planowanie — bliźniak planu i dane drogowe (wymagania operatora 2026-09-07)

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| **Bliźniak planowania**: `plan_snapshot` — każda wersja planu (przypisania zlecenie→trip→zasób; autor człowiek/auto; czas) zapisywana od pierwszego dnia planowania | operator | BRAK | KOPIUJ — wchodzi do **B0** (bez snapshotów nie ma „co by było gdyby") | B0 |
| **Kontrfaktyczne przeplanowanie**: „linie drobnicowe do NO/DE/SE zaplanowane inaczej (wg zapytania), reszta bez zmian → jak marża i czy plan wykonalny przy ówczesnym traficu/warunkach" | operator | BRAK | KOPIUJ — silnik na `plan_snapshot` + warunkach historycznych + optymalizatorze klasy OptiPlaner; marżę liczy SQL na `charge` | V (dane od B0) |
| **Własne historyczne TT**: każdy wykonany stop/trip = punkt danych (relacja, dzień tygodnia, godzina, sezon, rzeczywisty czas przejazdu) — własna baza czasów przejazdu rośnie od dnia 1, bez licencji | MC | BRAK | KOPIUJ — z actuals stopów (T1) przez `entity_event` (B0) | B0→V |
| Traffic zewnętrzny live + historyczny (HERE / TomTom / PTV) do ETA i TT | MC | BRAK | KOPIUJ | V/HZ (płatne — rachunek kosztów przed zakupem) |
| Pogoda: Open-Meteo (darmowe), IMGW (PL) — czynnik ETA/spalania/ryzyka | MC | BRAK | KOPIUJ | V |
| Restrykcje drogowe (wymiary, waga, naciski osi, ADR, tunele): **NAPSPAN** (agregator krajowych NAP + OSM; 15 jurysdykcji VIII 2026, rośnie) · OSM · krajowe NAP/DATEX II (darmowe) → upgrade płatny HERE/PTV truck attributes | MC | BRAK | KOPIUJ | V/HZ |
| Dokładne opłaty drogowe (klasa, osie, emisja, odcinek; e-TOLL PL stawki publiczne; wzorzec SPEED: myto z mapy prosto w koszty zlecenia) | MC/S | BRAK | KOPIUJ | V/HZ |
| **Zakazy jazdy** (niedziele, święta, wakacje, upały — kraj po kraju): **Nakordoni Truck Bans API** (38 krajów, typy General/Local/Sunday/Holiday/Seasonal, okna active/next w strefie kraju, wagi minimalne; darmowy feed JSON + API dev — TO_VERIFY licencja/atrybucja) + **Holiday Calendar API** (Nager.Date / OpenHolidaysAPI, darmowe) + własny katalog `driving_ban_rule` jako dane wersjonowane per jurysdykcja (MC §84); etransport.pl / trans.info = źródła redakcyjne do kuracji, nie API | operator | BRAK | KOPIUJ | V — ale katalog + odczyt feedu to czysta tabela, może wejść wcześnie |
| SENT przy planowaniu: flaga zlecenia SENT + GEO lokalizator widoczne na boardzie; zgłoszenia PUESC = C1 | S/MC | BRAK | KOPIUJ | T6 (flaga) + C1 (zgłoszenia) |

### 13e. Trzeci przegląd źródeł (2026-09-07, 21:20) — domknięcie inwentarza

Metoda: 103 sekcje master-contextu odhaczone 1:1 + digesty PDF 1–3 + dossier SPEED + 59 newsów + 44 case'y. Każda pozycja źródeł ma odtąd wiersz w § 1–13 **albo** wpis w Rejestrze odrzuceń niżej.

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Compliance / Legal Engine — reguły prawne wersjonowane per jurysdykcja (`effective_from/to`, źródło, wyjątki); pierwszy przypadek użycia: `driving_ban_rule` | MC §18/§84 | BRAK | KOPIUJ — fundament pod C/V; reguła = dane | C/V (katalog wcześnie) |
| Agenci doradczy AI: Transport / ADR / Customs / Legal Advisor — odpowiedź zawsze z podstawą prawną, jurysdykcją i wersją reguły; LLM cytuje, nie orzeka | MC §15/§17/§53 | BRAK | KOPIUJ | HZ (po Compliance Engine) |
| Wirtualne biuro rozliczeń czasu pracy kierowcy (naruszenia, dokumentacja kontrolna, zestawienia dla kadr) | MC §16 | BRAK | KOPIUJ | V7 → HZ (usługa) |
| Remuneration engine: płaca minimalna per kraj, delegowanie (2020/1057), dodatki, diety | MC §19 / S | BRAK | KOPIUJ | F5/HZ (prawo per kraj TO_VERIFY) |
| Network / resource costing: koszt pustych km, koszt niewykorzystania zasobu, wpływ zlecenia na następne zlecenia | MC §20 | BRAK | KOPIUJ | P/V (po T2) |
| Fleet cost model (financial driver costing): leasing, amortyzacja, opony, ubezpieczenia, serwis → pełny koszt km własnego taboru; karta drogowa, zaliczki | MC §78 / S (FTL) | BRAK | KOPIUJ | F/V (po T2) |
| Loading optimizer (bin packing: wymiary, piętrowanie, naciski osi, DMC) + VRP 1000+ dostaw | MC §21–22 | BRAK | KOPIUJ — silnik OR, nie LLM | V/HZ |
| Rejestr polis (własne + przewoźników: OCS/OCP/komunikacyjne — numer, suma, ważność; nadzór przy planowaniu i na kontrahencie) | S | BRAK | KOPIUJ | M-10/T2 pogłębienie |
| Ubezpieczenie cargo per zlecenie (polisa, suma, waluta; flaga na zleceniu jak SPEED) | S / MC | BRAK | KOPIUJ | F/HZ |
| Gospodarka oponami / serwis / przeglądy (fleet maintenance; łączy się z diagnostyką §13c) | S / MC §6 | BRAK | KOPIUJ | HZ (po telematyce) |
| Import / migracja danych: klienci archiwalni, kursy historyczne, schematy importu per tenant (wzorzec SID ze SPEED) | MC §68 / S | BRAK | KOPIUJ | przy onboardingu tenanta (po S53) |
| Kanały powiadomień SMS / e-mail (kierowca, klient, partner; bramki SMS) | S / MC | CZĘŚĆ (operator_notice M-34 = inbox wewnętrzny) | ULEPSZ | X |
| Dock scheduler — okna czasowe doków magazynu (awizacje D3 + sloty doków) | PDF (groupage) | BRAK | KOPIUJ | D3 |
| Sandbox / środowisko demo per tenant (standard wdrożeń z case'ów Qargo; kontra na „łzy" wdrożeń SPEED) | Q cases | BRAK | KOPIUJ | X/HZ (onboarding) |
| Widok brakujących kosztów per linia (wzorzec „Trips to Bill: Charge View") | Q | BRAK | KOPIUJ | F (rentowność tripa) |
| Fiscal risk scoring podmiotu (biała lista, status VAT, anomalie KSeF — podmiot, nigdy osoba) | PDF | CZĘŚĆ (C3 lookupy) | ULEPSZ | C/F |
| Claims deadline engine: terminy reklamacyjne, podstawa prawna, odpowiedzialność, timeline dowodów (CMR, GPS, temperatura) | PDF / MC §62 | CZĘŚĆ (M-55 tabela) | ULEPSZ | F/V |
| Auto-wystawienie kontenera/ładunku na giełdę (potrzeba → publikacja → zbiór ofert → propozycja) | MC §70 | BRAK | KOPIUJ | HZ (giełdy po umowach) |
| Integration Hub — abstrakcja protokołów (REST / SOAP / EDI / SFTP / AS2 / portal-fallback) pod konektory portów/armatorów/sieci | MC §95A / PDF | BRAK | KOPIUJ | HZ (z pierwszym konektorem) |
| Certyfikacja ISO 27001 / postawa NIS2 (argument sprzedażowy Qargo) | Q news | — | decyzja biznesowa | HZ (ops) |
| Prognozy cen frachtów/paliwa z czynnikami geopolitycznymi (korelacja ≠ przyczynowość) | MC §43 | BRAK | KOPIUJ | V/HZ (część Market Intelligence) |

## Rejestr odrzuceń — co świadomie NIE wchodzi i dlaczego (do decyzji operatora)

| Pozycja | Powód odrzucenia / odroczenia | Status |
|---|---|---|
| Przepisanie stosu na Django/GraphQL/Apollo/Zustand/Ant/Linaria | Zero zysku domenowego; utrata 128 przetestowanych plastrów; [ADR-0004](../adr/0004-benchmark-qargo-speed-2026.md) | ODRZUCONE na stałe |
| Konfiguracja cenników przez ręczne procedury T-SQL (mechanizm SPEED) | Każde wdrożenie = nieutrzymywalny dialekt; ostrzega własna instrukcja producenta; funkcja zostaje (cenniki warunkowe jako dane, Fala P) | ODRZUCONY mechanizm, funkcja wchodzi |
| Kopiowanie kodu, brandingu, grafik, tekstów dokumentacji Qargo/SPEED | Prawo autorskie + budujemy własną tożsamość; odtwarzamy funkcjonalność i wzorce UX | ODRZUCONE na stałe |
| Auto-scoring kredytowy JDG / osób fizycznych | AI Act (wysokie ryzyko) + art. 22 RODO; fakty + raport wywiadowni + decyzja człowieka (HITL) | ODRZUCONE na stałe (prawo) |
| Współpraca z osobami prywatnymi (B2C) | Decyzja operatora 2026-09-07; egzekwowana technicznie: rekord bez identyfikatora biznesowego nie powstanie (M10-1) | ODRZUCONE na stałe (biznes) |
| BIK / systemy bankowe do weryfikacji | Decyzja operatora 2026-09-07; zostają: KRD (formalnie BIG), Coface, D&B, CreditSafe, rejestry jawne | ODRZUCONE (decyzja) |
| WhatsApp / komunikatory | Mały zysk vs koszt integracji Meta dziś; luka rynku wg case'ów — wraca przy portalach | ODROCZONE → HZ |
| Energy Intelligence (floty EV, energia magazynów) | Brak popytu u docelowych klientów dziś | ODROCZONE → HZ |
| Mikroserwisy; osobne warstwy time-series / search / analytics | Przedwczesne przy obecnej skali; modular monolith + Postgres (CP-03); wraca przy realnych wolumenach | ODROCZONE (skala) |
| Temporal / Hatchet / workery | Standing rule repo: dopiero przy realnym konsumencie zdarzeń między BC (da go X4) | ODROCZONE (warunek) |
| Landing page www / cennik marketingowy („oferta w 8 minut", kalkulator wartości z §2 MC) | To osobny artefakt marketingowy (np. Astro), nie moduł aplikacji; nie blokuje produktu | POZA REPO produktu |
| Wyceny spółki, modele GMV/ARR/EBITDA z PDF | Materiał biznesowy, nie funkcjonalność; zostaje w `docs/_source/benchmark/` jako referencja | POZA MATRYCĄ |
| Scraping portali WCA / giełd / terminali bez umów | ToS + prawo; tylko oficjalne API po umowach (HZ) | ODRZUCONE na stałe |
| RAG/pgvector na logice wyceny, VAT, schemacie DB | HC-08: RAG wolno tylko na SOP/regulacjach/mailach/dokumentacji | ODRZUCONE na stałe (HC) |
| Deklarowanie „100% zgodności prawnej" / auto-reprezentacja celna bez upoważnienia | MC §18/§53: architektura pod zgodność ≠ gwarancja prawna; przedstawiciel celny wymaga umocowania | ODRZUCONE na stałe |
| „AI przewiduje przyszłość" jako obietnica marketingowa | MC §9/§99: komunikujemy zmierzoną skuteczność (Prediction Ledger), nie magię | ODRZUCONE na stałe |

## Przewaga nad Qargo i SPEED (cel: lider)

1. **Wieża z łańcuchem skutków** — visibility → prediction → impact → decision → execution; klient korporacyjny widzi, co się stanie z magazynem/produkcją/sprzedażą/EBITDA, **jeśli nie zareaguje**. Potwierdzone jako wolna pozycja (Qargo road-first bez shipperów; SPEED bez predykcji).
2. **Prediction Ledger** — każda predykcja mierzona po fakcie (MAE/kalibracja/coverage); dowód jakości zamiast „AI przewiduje".
3. **Multimodal + finanse + celny + faktoring w jednym modelu danych** z RLS — łańcuch wycena → zlecenie → faktura → bank → NBP → rozliczenia już działa.
4. **AI z HITL i audytem** (AI Act minimal risk) — ekstrakcja → wycena → zlecenie w produkcie; reguły i podsumowania dojdą jako dane + HITL, nigdy autonomiczny zapis.
5. **Web-native multi-tenant od dnia 1** — iSPEED dopiero startuje; Qargo web, ale bez PL-compliance (KSeF/SENT/biała lista). Czas-do-wartości i konfiguracja jako dane = kontra na największy ból wdrożeń SPEED.

## Świadome POMIŃ (funkcja ≠ mechanizm)

Stack Qargo (Django/GraphQL/Apollo/Ant/Linaria) · konfiguracja przez ręczne procedury T-SQL · polskie nazwy kolumn w bazie · branding/kod/assety obu systemów · WhatsApp (teraz) · drugi grid engine.
