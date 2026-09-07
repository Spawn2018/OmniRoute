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

## Przewaga nad Qargo i SPEED (cel: lider)

1. **Wieża z łańcuchem skutków** — visibility → prediction → impact → decision → execution; klient korporacyjny widzi, co się stanie z magazynem/produkcją/sprzedażą/EBITDA, **jeśli nie zareaguje**. Potwierdzone jako wolna pozycja (Qargo road-first bez shipperów; SPEED bez predykcji).
2. **Prediction Ledger** — każda predykcja mierzona po fakcie (MAE/kalibracja/coverage); dowód jakości zamiast „AI przewiduje".
3. **Multimodal + finanse + celny + faktoring w jednym modelu danych** z RLS — łańcuch wycena → zlecenie → faktura → bank → NBP → rozliczenia już działa.
4. **AI z HITL i audytem** (AI Act minimal risk) — ekstrakcja → wycena → zlecenie w produkcie; reguły i podsumowania dojdą jako dane + HITL, nigdy autonomiczny zapis.
5. **Web-native multi-tenant od dnia 1** — iSPEED dopiero startuje; Qargo web, ale bez PL-compliance (KSeF/SENT/biała lista). Czas-do-wartości i konfiguracja jako dane = kontra na największy ból wdrożeń SPEED.

## Świadome POMIŃ (funkcja ≠ mechanizm)

Stack Qargo (Django/GraphQL/Apollo/Ant/Linaria) · konfiguracja przez ręczne procedury T-SQL · polskie nazwy kolumn w bazie · branding/kod/assety obu systemów · WhatsApp (teraz) · drugi grid engine.
