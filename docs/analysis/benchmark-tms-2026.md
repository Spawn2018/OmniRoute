# Benchmark TMS 2026: Qargo + interLAN SPEED + wizja OmniRoute — matryca unii funkcjonalności

**Data:** 2026-09-07 · **Decyzja:** [ADR-0004](../adr/0004-benchmark-qargo-speed-2026.md) · **Kolejka:** [kolejka-propozycja.md](kolejka-propozycja.md) (propozycja, nie kanon) · **Pola:** [karty-pol-fala-t.md](karty-pol-fala-t.md)  
**Inwentarz MC+PDF (audyt „wszystko albo odrzucone”):** [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md)  
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
| Lejek oferty: wysłanie → otwarcie maila → otwarcie PDF → odpowiedź → konwersja (czasy w SQL) | operator 2026-09-07 | BRAK | KOPIUJ — §13i | X7 |
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
| Podkłady map: wiele darmowych (włącz/wyłącz w ustawieniach użytkownika) + płatne BYO API u admina tenanta | operator 2026-09-07 | BRAK | KOPIUJ — §13k | T6 + X8 |
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
| Etykiety + skanowanie kodów (walidacja wg trasy/statusu) | S/MC/Q | BRAK | KOPIUJ — §13n | D2 + D9 |
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
| Adapter ERP/FK (Comarch, Symfonia, Subiekt + reszta) — Omni **wystawia** FV; do FK idą przychodowe i kosztowe | operator 2026-09-07 | BRAK | KOPIUJ — §13l | F9 |
| Cyfrowa książka nadawcza (Poczta Polska: EN + śledzenie + EPO) | operator 2026-09-07 | BRAK | KOPIUJ — §13p | F11 |

## 8. Celna / compliance

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| SENT + odpowiedniki krajowe + EMCS/NCTS/DIWASS (katalog schem, nie jeden endpoint) | S/MC/operator | BRAK | KOPIUJ — §13h | C1 + C7 |
| AIS-IMPORT / AES / ZEFIR / OSOZ2 / PUESC | S/MC | BRAK | KOPIUJ (dostęp TO_VERIFY) | C |
| Intrastat | S | BRAK | KOPIUJ | C |
| Sankcje screening: kontrahent + **UBO + bank + HS/CN + port** (statki/ładunki/trasy) | MC / PDF s.183–184 | DONE M-53 | ULEPSZ — ten sam wiersz M-53, nie nowy silos | C/V |
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
| Telematyka: **bez własnych urządzeń** — Teltonika + Queclink (pakiet Omni) + hub API obcych platform + widoczność giełd; okno obserwacji związane ze zleceniem | operator 2026-09-07 | BRAK | KOPIUJ — §13g | V5 + V5b |
| Tachograf / czas pracy / Pakiet Mobilności / promy art. 9 561/2006 | S/MC | BRAK | KOPIUJ | V/HZ |
| Chłodnie: temperatura, alarmy, zdalne sterowanie | MC | BRAK | KOPIUJ (per urządzenie TO_VERIFY) | HZ |
| Watchtower: łańcuch skutków shipment → stock → produkcja → sprzedaż → EBITDA; „co jeśli nie zareagujesz" | MC | CZĘŚĆ (S32 liczniki) | ULEPSZ — przewaga nr 1 | V |
| What-if / scenario engine (port zamknięty, paliwo, bankructwo przewoźnika) | MC | BRAK | KOPIUJ | V/HZ |
| War room zakłóceń (7–10 kroków reakcji) | MC | BRAK | KOPIUJ | HZ |
| Digital twins (pojazd, kierowca, kontener, terminal, sieć) | MC | BRAK | KOPIUJ | V/HZ |
| Pogoda **cała Europa** (Open-Meteo wzdłuż trasy; IMGW/DWD/Météo-France = suplement) | MC/operator | BRAK | KOPIUJ — §13h | V |
| Toll engine precyzyjny **każdy kraj EU/EFTA** (klasa, osie, emisja/CO₂, odcinek, data; winiety osobno) | S/MC/operator | BRAK | KOPIUJ — §13h | V/HZ |
| Scoring przewoźnika: Trans.eu rating + opinie + własne KPI | S/Q/operator | CZĘŚĆ (M-13) | ULEPSZ — §13h | C9 + V |

## 10. AI

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Email → RFQ/wycena (klasyfikacja, ekstrakcja, dopasowanie kontrahenta) | Q/MC | DONE fundament | ULEPSZ (draft zlecenia z maila) | T4/X |
| Document Intelligence: enhance+kadr + split (podgląd z ramkami / pola z pewnością / edycja) + diff vs zlecenie | Q/ADR-0003 | CZĘŚĆ (M-20 split, bez bbox i enhance) | ULEPSZ — §13o | X6 + X9 |
| AI summaries wątków mailowych | Q | BRAK | KOPIUJ (Art. 50 label) | HZ |
| Chat-based validation rules (opis słowami → reguła jako dane → test na próbie → aktywacja) | Q/MC | BRAK | ULEPSZ | HZ |
| AI chat agent (pytania o rekordy i system) | Q | CZĘŚĆ (M-57 copilot) | ULEPSZ | HZ |
| Carrier procurement agent (RFQ → odpowiedzi → ranking) | MC | CZĘŚĆ (M-30/M-31 ślad) | ULEPSZ | HZ |
| CFO narracja po SQL (LLM nie liczy) | MC | DONE M-15/S57 | JEST | 0 |
| Zasada: LLM orkiestruje, silniki liczą | MC | DONE (HC-02) | JEST | 0 |

Kanon i liczby: [ai-nauka-i-dowody.md](ai-nauka-i-dowody.md), [ai-case-study-tms.md](ai-case-study-tms.md), [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md). HITL extract ma benchmark DocILE (Šimsa et al. 2023, ICDAR): LayoutLMv3 KILE F1 0,698, LIR F1 0,721 — residual błąd pól, nie vendor „99%”. Autonomiczny zapis ma pomiar przeciw: Goddard et al. 2012 (*JAMIA*) RR 1,26 (95% CI 1,11–1,44); Skitka et al. 1999 commission 3,92/6 (dokładność 35%). LLM nie liczy: PAL GSM-HARD CoT 20,1% vs interpreter 61,2% (Gao et al. 2023). GAN SR cyfr na skanie FV jest odrzucony (Zyrek et al. 2025: halucynacja glifów). ETA = ML + MAE/Prediction Ledger (Evmides 2024 MAE 99,9 min; project44 +28 pp @ 10 h ±2 h), nie LLM. Qargo −75% adminu = slogan (brak N i definicji jobu); mierzalny rząd to minuty na order entry w named case (Joda Freight 15→2 min, Pass 5 min→30 s–2 min), nie FTE. Copilot budowniczego: lab Peng 2023 (−55,8% czasu na HTTP server) ≠ RCT Cursor Pro na własnym OSS (METR/Becker 2025: +19% czasu); BRAK ŹRÓDŁA, że Copilot redukuje leftover.

## 11. Platforma

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Saved views (kolumny, filtry) + gęstość compact | Q | DONE (`table_view`, DataTableShell) | JEST | 0 |
| Współdzielenie widoków (prywatny / zespół / organizacja) | Q | CZĘŚĆ (widok per user) | ULEPSZ | X |
| Konfiguracja jako dane (anty-wzorzec SPEED: T-SQL per wdrożenie) | S/MC | DONE M-03 | JEST — lepszy mechanizm | 0 |
| Słowniki per tenant + teksty ustaleń + szablony | S | CZĘŚĆ | ULEPSZ | T7/D |
| Szablony dokumentów / wydruki (CMR, etykieta sieci, HBL, zlecenie, FV) | S/MC/Q | CZĘŚĆ (U-print ID, M-26) | ULEPSZ — §13n | D9 + F |
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
| Pogoda **cała Europa**: Open-Meteo (globalny, darmowy) wzdłuż geometrii `trip` (punkty, nie tylko PL); IMGW / DWD / Météo-France = suplement narodowy, nie jedyne źródło | MC/operator | BRAK | KOPIUJ — §13h | V |
| Restrykcje drogowe (wymiary, waga, naciski osi, ADR, tunele): **NAPSPAN** (agregator krajowych NAP + OSM; 15 jurysdykcji VIII 2026, rośnie) · OSM · krajowe NAP/DATEX II (darmowe) → upgrade płatny HERE/PTV truck attributes | MC | BRAK | KOPIUJ | V/HZ |
| Dokładne opłaty drogowe **w każdym kraju EU/EFTA**: klasa, osie, emisja/CO₂, odcinek, data; winiety jako osobny rodzaj; myto z mapy → `charge` z `source_ref` (wzorzec SPEED) | MC/S/operator | BRAK | KOPIUJ — §13h | V/HZ |
| **Zakazy jazdy** (niedziele, święta, wakacje, upały — kraj po kraju): **Nakordoni Truck Bans API** (38 krajów, typy General/Local/Sunday/Holiday/Seasonal, okna active/next w strefie kraju, wagi minimalne; darmowy feed JSON + API dev — TO_VERIFY licencja/atrybucja) + **Holiday Calendar API** (Nager.Date / OpenHolidaysAPI, darmowe) + własny katalog `driving_ban_rule` jako dane wersjonowane per jurysdykcja (MC §84); etransport.pl / trans.info = źródła redakcyjne do kuracji, nie API | operator | BRAK | KOPIUJ | V — ale katalog + odczyt feedu to czysta tabela, może wejść wcześnie |
| Flaga monitoringu na boardzie (SENT / EKAER / RO e-Transport / EMCS / odpad…) + GEO; zgłoszenia = C1/C7 | S/MC/operator | BRAK | KOPIUJ — §13h | T6 (flaga) + C1/C7 |

### 13e. Trzeci przegląd źródeł (2026-09-07, 21:20) — domknięcie inwentarza

Metoda (uczciwość 2026-09-07, 22:00; dociągnięcie nazw PDF: 13q): wcześniejsze zdanie „103 sekcje odhaczone 1:1” dotyczyło **nagłówków** MC, nie każdej funkcji/pola z PDF (376 s.). Audyt ziarna funkcji: [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md) · luki nazw: [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md). Każda pozycja ma wiersz w § 1–13q **albo** wpis w Rejestrze odrzuceń. Karty pól — przy `/plan-modul` (ADR-0004), nie tu.

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Compliance / Legal Engine — reguły prawne wersjonowane per jurysdykcja (`effective_from/to`, źródło, wyjątki); pierwszy przypadek użycia: `driving_ban_rule` | MC §18/§84 | BRAK | KOPIUJ — fundament pod C/V; reguła = dane | C/V (katalog wcześnie) |
| Agenci doradczy AI: Transport / ADR / Customs / Legal Advisor — odpowiedź zawsze z podstawą prawną, jurysdykcją i wersją reguły; LLM cytuje, nie orzeka | MC §15/§17/§53 | BRAK | KOPIUJ | HZ (po Compliance Engine) |
| Wirtualne biuro rozliczeń czasu pracy kierowcy (naruszenia, dokumentacja kontrolna, zestawienia dla kadr) | MC §16 | BRAK | KOPIUJ | V7 → HZ (usługa) |
| Remuneration engine: płaca minimalna per kraj, delegowanie (2020/1057), dodatki, diety | MC §19 / S | BRAK | KOPIUJ | F5/HZ (prawo per kraj TO_VERIFY) |
| Network / resource costing: koszt pustych km, koszt niewykorzystania zasobu, wpływ zlecenia na następne zlecenia | MC §20 | BRAK | KOPIUJ | P/V (po T2) |
| Fleet cost model (financial driver costing): leasing, amortyzacja, opony, ubezpieczenia, serwis → pełny koszt km własnego taboru; karta drogowa, zaliczki | MC §78 / S (FTL) | BRAK | KOPIUJ | F/V (po T2) |
| Loading optimizer (bin packing: wymiary, piętrowanie, naciski osi, DMC) + VRP 1000+ dostaw | MC §21–22 | BRAK | KOPIUJ — silnik OR, nie LLM | V/HZ |
| Rejestr dokumentów przewoźnika + **blokada zlecenia** gdy polisa wygasła / składka nieopłacona / licencja wygasła; odblokowanie po nowym ważnym dokumencie | S/operator | BRAK | KOPIUJ — §13h | C8 (po T2) |
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

### 13f. Silnik przetargowy głębiej + metrologia UX/UI (wymagania operatora 2026-09-07, 21:24)

Przetargi (rozwinięcie wiersza „Tender management" z 13c — pięć funkcji):

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Analiza dokumentacji przetargowej (RFP/SIWZ → wymagania, terminy, kryteria oceny, ryzyka, matryca zgodności) | MC §45 | BRAK | KOPIUJ — ekstrakcja wzorem M-20 (HITL), nie auto-odpowiedź | HZ (Tender) |
| **Playbook przetargowy**: strategia, argumenty, sugerowane ceny, analiza konkurencji („kto z kim współpracuje") — generowany dokument z provenance każdego twierdzenia | MC §45 / operator | BRAK | KOPIUJ — szkic zatwierdza człowiek | HZ (Tender) |
| **Prospecting**: lista firm do kontaktu z danymi z internetu (nazwa, mail, telefon, dlaczego warto, co to da, możliwe minusy) | operator | BRAK | KOPIUJ — research AI z podanym źródłem KAŻDEJ informacji; wynik = szkic kontaktu do CRM (HITL, dedup po NIP z M10-1); cold-outreach wg prawa PL (PKE/UŚUDE — zgody na kontakt elektroniczny, TO_VERIFY prawnik); **nigdy auto-send** | HZ (z CRM) |
| **Auto-wypełnianie matrycy przetargowej klienta** (Excel/portal) własnymi cenami albo cenami podwykonawców — „bez błędów" | operator | BRAK | KOPIUJ — determinizm: liczby WYŁĄCZNIE z pricing engine / cen wgranych (LLM mapuje format kolumn, nigdy nie liczy); walidacja schematu → diff-podgląd komórka po komórce → akceptacja człowieka; każda komórka z provenance (skąd cena); licznik błędów per przetarg = metryka (cel 0) | HZ (po Fali P) |
| **Bid/no-bid — wpisanie tras z matrycy w obecną sieć**: wykorzystanie zasobów, puste km, kolizje z obecnymi klientami → korzyści, zagrożenia, **wpływ na rentowność obecnego biznesu** | operator | BRAK | KOPIUJ — network costing (13e) + what-if na `plan_snapshot` (B0); marżę liczy SQL na `charge` | V (dane zbierane od B0) |
| Pomiar skuteczności przetargów: predykcja rentowności vs rzeczywistość po wygraniu; won/lost vs cena; kalibracja | operator | BRAK | KOPIUJ — wiersze w `prediction_ledger` | B0 → V |

Metrologia UX/UI (naukowa i techniczna):

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| Telemetria produktowa PostHog (zdarzenia, adopcja widoków/filtrów) | ADR-0002 | **DONE od plastra 0.5** | JEST | 0 |
| **Pomiar czasu jobu operatora** (wycena, accept HITL, zlecenie — od wejścia do zamknięcia; cel jakości PLAN: „job w czasie, który da się zmierzyć") | PLAN / MC | CZĘŚĆ (PostHog jest; brak nazwanych metryk jobów) | ULEPSZ — nazwane joby + funnel + czas + liczba błędów; każdy nowy ekran definiuje swój job-metric | T6/X (standard przy każdym nowym UI) |
| Budżety techniczne: initial JS < 250 kB (egzekwowane w CI) · p95 API < 150 ms · LCP < 1,5 s | AGENTS | CZĘŚĆ (size-limit działa; k6 stub; LCP bez RUM) | ULEPSZ — RUM Web Vitals przez PostHog + realny pomiar p95 na żywym ruchu | V/ops |
| A/B testy zmian UI (feature flags PostHog) — zmiana interfejsu = hipoteza + pomiar przed/po (czas jobu, błędy) | propozycja | BRAK | KOPIUJ | X/HZ |
| Dostępność: axe + Playwright w gate | ADR-0002 | CZĘŚĆ (3 ścieżki e2e; U-playwright-axe ID otwarte) | ULEPSZ wg U-* | Wave FE |
| Testy zadaniowe z pilotami (czas, błędy, SUS po sesji) przy onboardingu tenantów | propozycja | BRAK | KOPIUJ | X (piloty) |
| Lejek oferty po stronie **klienta** (otwarcie maila/PDF, czas do odpowiedzi, konwersja) | operator | BRAK | KOPIUJ — §13i; to nie PostHog (PostHog = nasi operatorzy) | X7 |

### 13g. Hub telematyczny + giełdy (decyzja operatora 2026-09-07: zero własnego HW)

**Dylemat 1 — nie każdy weźmie naszą telematykę, a bez pozycji nie działa ETA/wieża.**  
Rozwiązanie: jeden **Omni Telematics Hub**. Normalizuje pozycję do `PositionEvent` niezależnie od źródła. Źródło wybierane per pojazd / per `trip`, w tej kolejności:

1. **Pakiet Omni (opcjonalny)** — urządzenia **Teltonika** i **Queclink** (nie produkujemy; instalacja u przewoźnika, który chce). Protokoły z wiki producentów — TO_VERIFY per model.
2. **Bring-your-own-API** — przewoźnik podaje poświadczenia platformy + nr rejestracyjny. Sekrety szyfrowane kluczem tenanta (HC-05). Adapter mapuje płytę → `resource`.
3. **Aggregator** — gdy nie ma native adaptera: Linkway INTEGRATOR (~230 platform) albo DRIP (~400) — jeden kontrakt. TO_VERIFY umowa i cennik.
4. **Widoczność giełdowa** — jednorazowy podwykonawca bez apki i bez API: tracking **na serwis transportu**, nie na całą flotę.
5. **Poziom 0** — driver app / link SMS z geolokalizacją na czas zlecenia (zgoda kierowcy).

**Okno obserwacji związane ze zleceniem (RODO art. 5 — minimalizacja):**

```
trip.assigned(vehicle)     → start poll/subscribe (tylko ta płyta)
last_stop.completed        → grace N dni (domyślnie 3, konfiguracja M-03)
grace wygasa i brak nowego trip → STOP poll; kasuj cache live; sesja API wygasa
nowe zlecenie na tę płytę  → wznowienie
```

Nigdy: „obserwuj całą flotę przewoźnika 24/7, bo raz nam jechał". Historia pozycji z okresu zlecenia zostaje w `entity_event` (dowód ETA/reklamacji); live stream gaśnie.

**Dylemat 2 — giełda / jednorazowy kierowca + stawki z komunikatora.**

Tracking (oficjalne API — umowy TO_VERIFY):

| Giełda | Tracking | Komunikator / ceny |
|---|---|---|
| **Trans.eu** | TAK: `GET …/transports/{id}/monitoring` + `/trace` (pozycja, płyta, ETA, źródło GPS). Monitoring per **zadanie transportowe**, nie per flota. | Messenger do negocjacji — **brak publicznego API historii czatu** (IX 2026). Ceny: accepted price / oferty (osobne API, już w matrycy). |
| **TIMOCOM** | TAK: Shipment Tracking API (status, ETA, GPS) + Tracking API; ~299 providerów telematyki po ich stronie. | Messenger — **brak publicznego API czatu**; zapowiadany eksport do pliku (TO_VERIFY). |
| **Transporeon** | TAK: Open Visibility API (pozycja + ETA per shipment, geofencing, reguły udostępniania). | Czat nie jest produktem do integracji TMS. |
| **Teleroute (Alpega)** | API publiczne = CRUD ofert fracht/pojazd (`api-docs.teleroute.com`). Visibility = Alpega/Wakeo — **osobny produkt**, nie T-Interface. | Brak API czatu. |

**Stawki z komunikatorów — prawo i technika:**

- **Wolno:** analizować rozmowy, w których **nasz tenant jest stroną** (nasz spedytor ↔ podwykonawca) — analogia do `inbound_message`. Wymaga oficjalnego API albo eksportu z konta tenanta + zgody pracownika w umowie. Wynik = `exchange_message` → ekstrakcja stawki HITL → `rate_line` z `source_ref`.
- **Nie wolno:** skrapować cudzych czatów, podsłuchiwać rozmów, w których nie jesteśmy stroną, omijać ToS giełdy. Art. 267 KK + RODO + ToS. W Rejestrze odrzuceń.
- **Diagnostyka „za drogo / brak aut / słaby spedytor" bez podsłuchu:**
  1. Cena publikowana i accepted price z API giełd (oficjalne).
  2. Pole `quoted_amount` na `carrier_inquiry` (M-30) — spedytor wpisuje / AI wyciąga z **naszego** maila/czatu.
  3. Metryki jobu spedytora (`entity_event`): czas do pierwszej odpowiedzi, liczba kontaktów, konwersja oferta→akceptacja, porównanie do mediany tenanta.
  4. Jeśli API da wyświetlenia oferty: wyświetlenia vs odpowiedzi vs nasza cena vs mediana lane — rozdziela „za drogo" od „nikt nie patrzył" od „spedytor nie odpisał".

**Polscy providerzy (API tam, gdzie potwierdzone publicznie, IX 2026):**  
Inelo **GBOX** (docs.gbox.pl) · **IKOL** (`api.ikol.pl`, `iaGetLocatorLastPosition`) · **Flotis** (REST: firmy/pojazdy/pozycje, Basic + api-key) · **Cartrack PL** (API po umowie) · **Navifleet** (własne API + ATLAS do TIMOCOM/Trans.eu) · **Flotman** · **SATIS GPS** (web services / TMS) · **GeoNAVI** · **NaviExpert Telematics** · **DataSystem** · Elte GPS · Finder · PlusFleet · Lokalizuj.com · iTrack · DigiTrack · Ecofleet · Movcar · partnerzy Wialon/Gurtam w PL · WebEye · Trimble/Transics (instalacje PL). Inflota = głównie opony/CFM, nie pełny GPS.  
**Tronik** (`tronik.pl`, platforma **ATRAX4** / Atrax GPS + Atrax TMS, apka KT4, T-Lock, e-TOLL, tacho): integracje TMS/ERP i giełdy; jest na Linkway INTEGRATOR jako ATRAX4. Publicznego swaggera nie ma — API/connector po umowie.  
**Logisat** (`logisat.pl`, panel `gps2.logisat.pl`): deklaruje REST API + dokumentację „na życzenie”; SENT GEO; gotowe konektory **Linkway** i **CO3** (login+hasło do konta GPS). Native adapter po dokumentacji; do tego czasu aggregator.  
Do weryfikacji API przy umowie (nazwy z rynku PL, nie P0): CMA Monitoring · Framelogic · AutoGuard · Locon · Yanosik Flota / Neptis · GannetGuard · Trakito · SmartFleet · Vialtis · T-Mobile Flota / MoveOn. Native adapter dopiero po dokumentacji.  
Adaptery P0: GBOX + IKOL + Flotis + Wialon (najczęstsze u PL przewoźników). Reszta: aggregator albo na żądanie. Rynek jest rozdrobniony — „wszyscy" = ta lista + nowi przez aggregator; native adapter nie powstaje bez umowy i dokumentacji.

**30 największych w Europie (Berg Insight, baza zainstalowana, koniec 2024):**  
Targa Telematics (~900k) · Webfleet (~752k) · CalAmp (~600k) · Verizon Connect (~500k) · Radius (~482k) · Scania (~461k) · Geotab · Microlise · Daimler Truck (~382k) · Volvo Group (~364k) · AddSecure Smart Transport (~320k HCV) · Eurowag Telematics · ABAX · Shiftmove · Gurtam/Wialon · Quartix · Bornemann · Michelin Connected Fleet · MAN (~264k) · SCALAR/ZF · Linqo · Cartrack · Powerfleet · RAM Tracking · Océan/Orange · Mapon · Platform Science · GSFleet · DAF · Macnil. Tuż za listą: AROBS · Actia · Iveco · Ctrack · Matrix iQ · Infobric · Teletrac Navman · Ruptela · Teltonika/Queclink (HW). Geotab po zakupie Verizon Connect EU (2025, poza Hiszpanią) awansuje na szczyt — TO_VERIFY przy implementacji.  
API potwierdzone publicznie: Webfleet.connect · Wialon SDK · Geotab MyGeotab · Trimble · Flotis · IKOL · GBOX. Pozostałe = TO_VERIFY przy umowie; do tego czasu aggregator.

### 13h. Pogoda pan-EU, odpady, blokada dokumentów, Trans.eu, SENT-europa, myto (operator 2026-09-07)

**Pogoda — cała Europa, nie tylko PL.**  
Źródło bazowe: **Open-Meteo** (darmowe, pokrycie globalne, więc cała Europa + kraje tranzytu poza UE). Pobór wzdłuż geometrii `trip` (punkty / odcinki), nie jeden punkt „kraj załadunku". IMGW (PL), DWD (DE), Météo-France = suplement, gdy tenant chce narodowy feed. Wynik = czynnik ETA/ryzyka w `entity_event`, nie liczba liczona przez LLM.

**Odpady — BDO kraj + transgranica.**

| Zakres | System | Integracja |
|---|---|---|
| PL krajowy | Rejestr BDO + KPO / KPOK | Oficjalne REST API (darmowe): `bdo.mos.gov.pl` / swagger test `test-bdo.mos.gov.pl`. Zmiana kontraktu API **1.01.2027** — projektować pod nową spec. |
| Tranzyt / załadunek / rozładunek przez PL | Wpis BDO także dla zagranicznego przewoźnika | Ten sam numer BDO na KPO/CMR |
| UE transgranica | WSR (UE) 2024/1157 od **21.05.2026**; do tego dnia 1013/2006 | **DIWASS** (KE): GUI + API dla oprogramowania komercyjnego (IR 2025/1290). Interop z eFTI. |
| Poza UE | Konwencja bazylejska + zgody PIC | Dokumenty na `shipment`; nie wymyślamy „światowego BDO" |
| Towary wrażliwe PL | SENT często **nakłada się** na odpad | Flaga SENT + flaga odpadu na tym samym zleceniu |

OmniRoute nie zastępuje BDO. Wystawia / potwierdza KPO przez API tenanta, trzyma numery i statusy na `shipment`, HITL przed zapisem. Kwot i mas nie liczy model.

**Blokada zlecenia — polisa / składka / licencja.**  
Tabela `party_document` (per tenant, RLS): rodzaj (`ocp` / `ocs` / `comm_insurance` / `community_licence` / `cemt` / `bdo_number` / `waste_permit` / inny jako dane), `valid_from`/`valid_to`, `premium_status` (`paid`/`unpaid`/`unknown`), `source_ref`.  
Brama przy `POST shipment` (i przy przypisaniu podwykonawcy do `trip`): brak wymaganego dokumentu **albo** `valid_to` < data załadunku **albo** `premium_status=unpaid` → **409**, zlecenie nie powstaje. Komunikat po polsku z listą braków.  
Odblokowanie: nowy wiersz z aktualnymi datami i `paid` (upload / extract HITL / sync z Trans.eu `documents.expire_date`). Stary wiersz zostaje (niemutowalna historia).  
Wymagany zestaw = dane w M-03 per relacja (krajowa vs międzynarodowa vs odpad). Nie scoring osoby. Nie auto-decyzja kredytowa.

**Trans.eu — scoring i opinie (oficjalne API, IX 2026).**  
`GET /ext/partners-api/v1/partners/{id}` zwraca: `overall_rating` (0–5), `contractors_satisfaction` (m.in. communication, documents_delivery, load_as_described, caring_for_goods, transport_on_time_performance…), `trans_risk` (SUPER…POOR), `payments_status`, `documents[]` z `expire_date`.  
Opinie słowne **są na platformie** (po transakcji, 120 dni, komentarz + tagi „co poszło nie tak"). **Publicznego endpointu listy komentarzy nie ma w dokumentacji** — TO_VERIFY u `api@trans.eu`. Do potwierdzenia: snapshot scoringu z API; komentarze tylko po oficjalnym API/eksporcie albo wklejenie HITL. Zakaz scrapingu profili. Snapshot na `party` z `source_ref` + czasem pobrania (wzorzec M-13). Próg blokady po niskiej ocenie = konfiguracja tenanta, nie twardy kod.

**Systemy „jak SENT" — katalog, nie mit „w każdym kraju jest SENT".**  
Większość krajów UE **nie ma** klona SENT dla zwykłego ładunku. Jest: (a) unijne systemy obowiązkowe, (b) kilka narodowych monitorów towarów wrażliwych / VAT, (c) reszta = brak analogu. Model: `monitoring_scheme` jako dane (kraj, rodzaj, urząd, API, czy GEO).

Unia (wszystkie państwa członkowskie + często EFTA):

| System | Co monitoruje |
|---|---|
| **EMCS** | Wyroby akcyzowe w procedurze zawieszenia |
| **NCTS** | Tranzyt celny |
| **e-TIR** | TIR w NCTS |
| **DIWASS** | Przemieszczanie odpadów (od 21.05.2026) |
| **eFTI** | Informacja regulacyjna w transporcie (cel 2027) |

Narodowe (potwierdzone; reszta TO_VERIFY przed adapterem):

| Kraj | System | Zakres |
|---|---|---|
| PL | **SENT + SENT-GEO** (PUESC) | Towary wrażliwe; GPS na czas zgłoszenia |
| HU | **EKAER** | Towary ryzykowne (VAT) |
| HU | **BIREG** | Zezwolenia / kabotaż / relacje z państw trzecich |
| RO | **RO e-Transport** (UIT) | Towary wysokiego ryzyka fiskalnego + transport międzynarodowy na terytorium RO |
| FR | **Trackdéchets** | Odpady niebezpieczne (nie ogólny fracht) |
| IT | **RENTRI** (następca SISTRI) | Odpady |
| ES | **SILICIE** | Ewidencja akcyzy (nie klon SENT) |
| DE | **ATLAS** | Cło / akcyza — nie monitor drogowy jak SENT |
| GR | ICSISnet | TO_VERIFY zakres |
| BG | e-Transport (ryzyko fiskalne) | TO_VERIFY ustawa i API |

SK, CZ, AT, NL, BE, LU, DK, SE, FI, IE, PT, EE, LV, LT, HR, SI, CY, MT oraz EFTA (NO/CH/IS/LI): **brak potwierdzonego klona SENT** dla ogólnego ładunku — obowiązują EMCS/NCTS + ewentualnie odpad/akcyza. Nie wymyślamy systemu, żeby „wypełnić mapę". Nowy kraj = nowy wiersz w katalogu po źródle prawnym.

P0 adapterów zgłoszeń: SENT (C1) · EKAER · RO e-Transport · BDO/KPO · DIWASS (gdy API integratora dostępne). Reszta = flaga + checklista dokumentów do ręcznego portalu.

**Myto precyzyjne w każdym kraju europejskim.**  
Nie ma jednego darmowego rządowego API na całą UE. Precyzja wymaga: trasa (geometria) + pojazd (DMC, osie, Euro, klasa CO₂) + data (taryfa wersjonowana). Winieta (czasowa) ≠ myto kilometrowe — dwa rodzaje `charge`.

Źródła (wybór po rachunku kosztów, nie wszystkie naraz):

- Komercyjne routing+toll: **PTV** (większość Europy, klasy 2022/62/WE), HERE, **NAPSPAN** (już w 13d), **TollCalc** (~37 krajów).
- Taryfy publiczne do kuracji: e-TOLL PL, Toll Collect DE, ASFINAG AT, HU-GO, ViaToll/myto SK/CZ, Viapass BE, LSVA CH, TollRo RO (od X 2026).
- EETS (Eurowag, Toll4Europe…) rozlicza przejazd — **nie zastępuje** silnika wyceny w TMS.

Wynik odcinka → `charge` z `source_ref` (które API, która taryfa, która data). Kolumna `charge.source_ref` nie istnieje dziś (migracja 009 + model) — leftover P0 Fali P: nullable na starych fixture, obowiązkowe na INSERT z myta i znaczka PP (F11). LLM/JS nie liczą. Brak taryfy dla odcinka = warning, nie zmyślona kwota.

### 13i. Lejek oferty: otwarcie maila, otwarcie PDF, odpowiedź, konwersja (operator 2026-09-07)

Cel: zmierzyć, czy klient w ogóle zobaczył ofertę i jak długo zwlekał — analogia do metryk spedytora z §13g, ale po stronie odbiorcy.

**Zdarzenia (append-only, RLS, `source_ref`).** Tabela `quote_engagement` albo wiersze w `entity_event` na `quotation` + `mail_draft`:

| Zdarzenie | Skąd wiemy | Pewność |
|---|---|---|
| `sent` | `mail_draft` → sent (mailto: operator potwierdza / Graph send daje znacznik) | wysoka przy Graph; średnia przy samym mailto |
| `delivered` | DSN / Graph delivery — TO_VERIFY per skrzynka | często brak |
| `email_opened` | unikalny piksel w HTML **tylko przy zgodzie** na `party_contact` | niska: Apple Mail Privacy prefetches, skanery antywirusa fałszują „otwarcie" |
| `pdf_viewed` | **hostowany PDF** pod jednorazowym `GET /q/{token}` (nie załącznik) | wysoka: klik + HTTP to konkretny dokument |
| `replied` | `inbound_message` dopięty wątkiem (`In-Reply-To` / numer oferty w temacie) | wysoka |
| `converted` | `offer_acceptance` won albo `shipment` z `quotation_id` | wysoka |
| `lost` | werdykt lost / wygaśnięcie ważności bez konwersji | wysoka |

**Czasy (SQL na znacznikach, nie Python/LLM/JS):**

1. `sent → email_opened` — czas do otwarcia maila  
2. `sent → pdf_viewed` — czas do przeczytania oferty  
3. `sent` (albo `delivered`, gdy jest) `→ replied` — czas od doręczenia/wysłania do odpowiedzi drugiej strony  
4. `pdf_viewed → replied` — czas od otwarcia oferty do odpowiedzi  
5. `sent → converted` oraz `pdf_viewed → converted` — konwersja  

Na tablicy wycen: te pięć liczb + flaga pewności (`prefetch` vs `human`). Mediana tenanta / spedytora / lane — do diagnostyki: „nie otworzył" vs „otworzył i nie odpisał" vs „odpisał za późno / odrzucił cenę".

**Technika (żeby działało już przy dzisiejszym mailto):**  
Załączony PDF **nie** da sygnału otwarcia. W ciele maila i w PDF: link `https://…/q/{token}` (token niezgadywalny, TTL = ważność oferty, jeden tenant). GET = `pdf_viewed`. Piksel w HTML tylko gdy kontakt ma `tracking_consent=true`. Bez Graph send piksel i tak często nie wyleci (klient Outlook może wyciąć HTML) — **link do PDF jest głównym sygnałem**. Portal klienta (X1) po zalogowaniu = ten sam event `pdf_viewed` (wyższa pewność).

**Prawo (twarde):**  
Piksel w mailu = odczyt z terminala (wytyczne EDPB 2/2023 art. 5(3) ePrivacy; CNIL IV 2026: zgoda na piksel **osobna** od zgody na sam mail, także B2B i transakcyjne). PL: PKE + RODO.  
- Piksel: tylko po zgodzie na kontakcie; stopka z wycofaniem jednym kliknięciem; bez zgody mail idzie bez piksela.  
- Klik w link oferty (świadoma akcja) + hostowanie u nas: podstawa = wykonanie umowy / uzasadniony interes wyceny B2B — TO_VERIFY prawnik; i tak informacja w stopce i polityce.  
- Zakaz: niewidoczny tracking bez zgody, tracker trzeciej strony (Mailchimp pixel w ofercie), sprzedaż zdarzeń, śledzenie osób prywatnych (B2C i tak odrzucone).  
- Dane zostają w tenancie (RLS). Token wygasa. Nie logujemy treści skrzynki klienta.

### 13j. Luki po audycie MC+PDF (2026-09-07, 22:00) — to, czego nie było jako osobny wiersz

Pełna mapa: [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md). Poniżej funkcje z PDF/MC, które wcześniej były tylko „w domyśle” albo ginęły w silniku nadrzędnym.

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| **Cost Allocation Engine** (DIRECT / SHARED / ALLOCATED / OVERHEAD / CAPITAL / RISK) → True Contribution Margin; koszt nie wisi wyłącznie na jednym zleceniu | PDF s.115–116 / MC §20 | CZĘŚĆ (marża na `charge`) | ULEPSZ — alokacja w SQL na `charge` + klucze alokacji jako dane | F/V (po T2) |
| **Make or Buy**: własny tabor vs giełda vs sieć drobnicowa — ten sam ładunek, koszt+ETA+FIX+prawo | PDF s.121 / MC §74 | BRAK | KOPIUJ | V (po T2+D8) |
| **TIME-TO-FIX**: SAFE / AMBER / RED + rozbicie przyczyn (korek, przerwa, prom, ograniczenie) | PDF s.89–90 | BRAK | KOPIUJ | V2 |
| **Dwa ETA**: fizyczne (kiedy auto dojedzie) vs prawne/operacyjne (kiedy wolno dojechać) | PDF s.98–99 | BRAK | KOPIUJ | V2+V7 |
| `FERRY_REST_EVENT` — prom ≠ zwykły stop (art. 9 561/2006) | PDF s.98 / MC §11 | BRAK | KOPIUJ | T1 (typ stopu) + V7 |
| **Ferry watchdog**: ETA portu vs cut-off; rebooking + wpływ na tacho i FIX | PDF s.53, 76 | BRAK | KOPIUJ | V3 analog (prom) |
| **Driver Time Solver**: warianty A–I (odpoczynek, split, ferry, multi-manning, drugi kierowca) | PDF s.97 | BRAK | KOPIUJ | V7 |
| **Legal Feasibility Check** przed przyjęciem zlecenia (godziny, ADR, posting, FIX) — wynik ryzyko, nie „wolno/nie wolno” od LLM | PDF s.111–112 | BRAK | KOPIUJ | C/V (po katalogu reguł) |
| **Compliance & Time Simulation** minuta po minucie (droga→korek→prom→odpoczynek→FIX) | PDF s.105 | BRAK | KOPIUJ | V7 |
| **Geofence → waiting**: ARRIVED → licznik postoju → po limicie propozycja waiting charge (HITL, nie auto-INSERT `charge`) | PDF s.51–53 | BRAK | KOPIUJ | V5 + P |
| Elektroniczna **karta drogowa** (GPS+tacho+CAN+paliwo+stopy+koszty) | PDF s.39–41 / S | BRAK | KOPIUJ | V7/F |
| **Fuel fraud / anomalia paliwa**: expected vs actual, tankowanie vs GPS; flaga do recenzji, nigdy wyrok „kradzież” | PDF s.48, 204–206 | BRAK | KOPIUJ | V/HZ |
| **Profil wysokości** trasy jako czynnik ETA/spalania (osobno od pogody) | MC §60 / PDF | CZĘŚĆ („pogoda / wysokość” w §9) | ULEPSZ — osobny input | V |
| **Słownik typów szkód** + Claims OS (15 kroków) + Deadline Engine | PDF s.207–210, 346 | CZĘŚĆ (M-55 + 13e) | ULEPSZ | F/V |
| **VAT Engine** (traktowanie + stawka + podstawa prawna + confidence; B2B only) | PDF s.139 | BRAK jako silnik | KOPIUJ — SQL + katalog reguł; LLM nie liczy VAT | F/C |
| **Terms AI** na druku obcego zlecenia (ryzyko operacyjne/finansowe/prawne + HITL) | PDF s.163–164 | CZĘŚĆ (13e import) | ULEPSZ | X |
| **Response Intelligence** (czasy RFQ→odpowiedź→oferta per strona) | PDF s.179 | CZĘŚĆ (13g metryki + 13i lejek) | ULEPSZ — jeden widok czasów | X7/V |
| **Linehaul Schedule Engine** + symulacja przesunięcia linii (OTD/koszt) | PDF s.152–158 | CZĘŚĆ (D1) | ULEPSZ | D1 + V (what-if) |
| **Consolidation Engine** (wiele shipmentów → 1 consol) | PDF s.180 | CZĘŚĆ (D6) | ULEPSZ | D6 |
| **Opportunity Engine** (oszczędność / koszt wdrożenia / ryzyko / ROI / owner) | PDF s.252 | BRAK | KOPIUJ | V/HZ |
| **Transformation Office** (inicjatywy vs zrealizowana oszczędność) | PDF s.200 | BRAK | KOPIUJ | HZ (wieża) |
| **Spend leakage** (kontrakt vs FV, podwójny FSC, free time) | PDF s.199 | CZĘŚĆ (Contract Intelligence §12) | ULEPSZ | HZ |
| **Dwie perspektywy, jeden core**: Operator OS (spedycja) + Enterprise (wieża klienta) | PDF s.254–255 | BRAK jako produkt | KOPIUJ — ten sam model, inny portal (X1 vs T6) | X1 + V6 |
| **Bliźniak urzędu** (proces/wymagania/deadline, nie udawanie urzędu) | PDF s.187–191 / MC | BRAK | KOPIUJ | C/HZ |
| **Carbon Data Layer ≠ raport ESG** (osobno dane i warstwa sprawozdawcza per standard) | PDF s.160 | CZĘŚĆ (C5) | ULEPSZ | C5 |
| **Karty naukowe** predykcji (model card / data card / prediction card) | PDF s.276+ | CZĘŚĆ (V1 ledger) | ULEPSZ | V1 |
| Unified Telemetry Model (pola: position, fuel, driver, CAN, DTC, temp, source) | PDF s.44, 61 | BRAK | KOPIUJ — kontrakt V5 | V5 |
| Cache tras (TTL: traffic 30–120s, trasa 5–30 min, LEZ do aktualizacji źródła) | PDF s.67 | BRAK | KOPIUJ | V (routing) |
| Akceptacja oferty z języka maila („akceptujemy 1850 EUR”) → szkic zlecenia, **HITL** | PDF s.125–126 | CZĘŚĆ (M-29) | ULEPSZ | X |
| P&O Freight API (nowe od 1.06.2026; stare EDI nie) | PDF s.70 | BRAK | KOPIUJ po umowie | HZ |
| Prom: sprzedaż z marżą, klient nie widzi ceny zakupu | PDF s.74–75 | CZĘŚĆ (`charge` buy+sell) | JEST mechanizm — użyć na nodze promu | T/P |
| Apka kierowcy **nie** „poprawia” tachografu — każdy wpis z audytem | PDF s.100 | BRAK | KOPIUJ | X3/V7 |
| Sześć pytań przy każdym nowym module (dane, połączenia, predykcja, wpływ, decyzja, pomiar) | PDF s.224 | — | reguła procesu `/plan-modul` | ops |
| Słownik naczep (Curtainsider, Mega, Reefer, Coilmulden…) + dane osiowe | PDF s.118–120 | BRAK | KOPIUJ | T2 |
| Label Engine (SSCC, sort code, hub) + wydruk wymagany przez sieć drobnicową + skan zwrotny na zlecenie | PDF s.151 / Q help / S | CZĘŚĆ (D2) | ULEPSZ — §13n | D2 + D9 |
| Dock time window (pola: dok, palety, typ naczepy, ADR, waga) | PDF s.135 | CZĘŚĆ (D3) | ULEPSZ | D3 |
| Bank Adapter Layer (CAMT/PAIN; mBank, PKO — nie bank na sztywno) | PDF s.137–138 | CZĘŚĆ (F4) | ULEPSZ | F4 |
| Credit warning przy limicie (przedpłata / podnieś limit / CFO) — podmiot | PDF s.139 | CZĘŚĆ (F6) | ULEPSZ | F6 |
| Photo POD quality check → „zrób zdjęcie ponownie” | PDF s.148 | CZĘŚĆ (X6) | ULEPSZ — §13o (gate + OpenCV, nie GAN) | X6 + X9 |
| FSC per usługa (nie jeden globalny %) | PDF s.156 / MC | CZĘŚĆ (P3) | ULEPSZ — reguła jako dane | P3 |
| Connected Carrier / finansowanie GPS (leasing, „darmowy GPS”, shipper płaci visibility) | PDF s.37–54 | BRAK | decyzja biznesowa; HW własny odrzucony | HZ |

Nazwane silniki z PDF, które nadal ginęły po §13j: **§13q**.

### 13k. Podkłady map — darmowe u użytkownika, płatne BYO u admina (operator 2026-09-07)

**Dwa poziomy, katalog jako dane (nie sztywny enum w kodzie):**

1. **Użytkownik** (`user_map_prefs`): lista darmowych podkładów — każdy włącz / wyłącz; ostatnio wybrany; przezroczystość nakładek. Dotyczy mapy planowania, wieży, tripa. Brak kluczy.
2. **Administrator tenanta** (`tenant_map_provider`): płatny dostawca + zaszyfrowany klucz (HC-05, nigdy w logach) + ograniczenie domeny z panelu dostawcy. Po zapisie podkład pojawia się u użytkowników tej organizacji. Instrukcja w UI i w [podklady-map-admin.md](podklady-map-admin.md).

Mapa zawsze lazy (poza initial 250 kB). Atrybucja obowiązkowa na dole mapy (ODbL / dostawca).

**Darmowe (P0 — bez klucza, z atrybucją):**  
OpenFreeMap (wektor, kilka stylów) · OpenTopoMap · CyclOSM · Humanitarian OSM (HOT) · Carto Positron / Voyager (warunki TO_VERIFY przy implementacji) · **GUGiK Geoportal** ortofotomapa + mapa topograficzna (WMTS, PL) · Esri World Imagery / World Street (atrybucja Esri; TO_VERIFY limit).  
**Zakaz:** `tile.openstreetmap.org` jako CDN produkcyjny (polityka OSMF). Self-host Protomaps/PMTiles = opcja admina (własny plik, bez klucza zewnętrznego).

**Płatne BYO (admin wkleja własne API):**  
Mapbox · MapTiler · Google Maps Platform · HERE · TomTom · PTV · Stadia Maps (Stamen) · Thunderforest · Jawg · Azure Maps · Esri ArcGIS · Geoapify · LocationIQ.  
Nowy dostawca = wiersz w katalogu (URL szablonu kafelka / style JSON + gdzie wziąć klucz) — nie nowy kod na każdego.

Nakładki (osobno od podkładu, też on/off): ruch live (gdy jest klucz), LEZ/restrykcje (NAPSPAN/OSM), kolej (OpenRailwayMap), **parking, paliwo (POI), granice, promy, cło, pogoda** (katalog danych; źródło per warstwa TO_VERIFY — §13q).

### 13l. ERP i księgowość — Comarch, Symfonia, Subiekt (operator 2026-09-07)

OmniRoute zostaje prawdą o **marży** (`charge`) i o **wystawieniu faktury**. ERP/FK zostaje prawdą o **dekrecie i JPK**. Adapter nie liczy VAT/marży i nie woła HTTP z BC `bookkeeping` (zakaz M-47). Składa to warstwa API + agent u klienta.

**Decyzja operatora (2026-09-07):** faktury **wystawia Omni** (KSeF = Omni, nie ERP). Do księgowości wysyłamy **oba typy**:

| Typ w Omni | W FK (Comarch / Symfonia / Subiekt) | Źródło |
|---|---|---|
| **Przychodowa** | dokument sprzedaży (FS / FV) | `sales_invoice` (M-40) + numer KSeF po wysyłce |
| **Kosztowa** | dokument zakupu (FZ / FV zakupu) | `purchase_invoice` — z maila / KSeF / skanu; podpinana pod zlecenie **dopiero po HITL** (§13m) |

ERP nie wystawia tych dokumentów od nowa. Dostaje gotowy dokument z Omni (kwoty już na fakturze; pochodzą z `charge`, nie z przeliczenia w adapterze).

**Co płynie (mapowanie jako dane, HITL przy pierwszym mapowaniu kont/serii):**

| Kierunek | Obiekty |
|---|---|
| Omni → ERP | `party` (NIP), FV przychodowa + KSeF ref, FV kosztowa + ewentualny KSeF nabycia, serie dokumentów |
| ERP → Omni | status płatności, numer w dzienniku FK, potwierdzenie zaksięgowania — **nie** nadpisuje kwot `charge` ani numeru FV Omni |
| Zakaz | zapis `charge.amount`; KSeF z ERP; surowy SQL do bazy klienta |

**KSeF:** `ksef_issuer` = **`omni` na stałe** (decyzja). ERP nie wysyła FA(3) dla tych samych dokumentów.

**P0 — polskie FK/ERP, które trzeba obsłużyć pierwsze:**

| System | Kanał (IX 2026) | Jak się łączy |
|---|---|---|
| **Comarch ERP Optima** | COM + Web/REST (często licencja API / partner); nie jeden darmowy swagger | Agent na Windows z Optimą albo chmura Comarch — BYO poświadczenia |
| **Comarch ERP XL** | Natywne **CDN API** (COM/SOAP); REST u partnerów, nie „oficjalny jeden REST XL” | Agent przy serwerze XL; stały host; TO_VERIFY licencja Comarch |
| **Symfonia** (Sage / Cegid) | Oficjalne **WebAPI REST/JSON** — sesja `OpenNewSession`, potem `Authorization: Session {guid}`; docs `pomoc.symfonia.pl` (edycja 2026) | URL instancji + klucz aplikacji (HC-05) |
| **InsERT Subiekt nexo** | **Sfera** (w nexo PRO wbudowana, inaczej dokupić) | Agent przy MSSQL + Sfera; nie otwieramy bazy na świat |
| **InsERT Subiekt GT** | Dodatek **Sfera dla Subiekta GT** | Ten sam model agenta; GT ≠ nexo — dwa adaptery |

**P1 (ten sam hub, kolejny wiersz katalogu):** enova365 WebAPI (REST+JWT, Swagger, moduł licencyjny) · WAPRO Mag/Fakir (WebAPI integrator) · Streamsoft · Reset2 · TETA.  
**EU:** SAP B1 Service Layer · Business Central OData · DATEV — HZ po P0.

Nowy system = wiersz w `erp_connector` (protokół, URL szablonów, czy wymaga agenta on-prem). Agent wychodzi **na zewnątrz** do Omni (outbound), sekrety szyfrowane, idempotencja na numerze dokumentu.

Instrukcja admina: [erp-fk-adapter.md](erp-fk-adapter.md).

### 13m. Zaciąganie FV kosztowych (mail / KSeF / skan) + dopasowanie do zlecenia (operator 2026-09-07)

Ten sam kontrakt co stawki (M-20): model **wyciąga**, SQL **szuka kandydatów**, człowiek **akceptuje**. Bez accept nie ma `purchase_invoice` na zleceniu i nic nie leci do FK.

**Trzy źródła → jeden `extraction_draft` (kind=`purchase_invoice`):**

| Źródło | Wejście | Parser |
|---|---|---|
| Mail | `inbound_message` + załącznik PDF | jak cennik: fingerprint → docling/tekst → instructor |
| KSeF zakup | oficjalne API 2.0: `POST /invoices/query/metadata` (Subject2) + `GET /invoices/ksef/{nr}` → XML FA(3) | **deterministyczny** (schemat XSD), nie LLM |
| Skan / papier | upload zdjęcia/PDF (kierowca, biuro, portal) | docling + OCR; jakość zła → „zrób zdjęcie ponownie” (jak Photo POD) |

Dedup: ten sam numer KSeF **albo** (sprzedawca + numer FV + data) = ten sam draft. `source_ref` obowiązkowy.

**Drabina dopasowania (SQL, nie model liczy score).** Każdy sygnał ma wagę; wynik = lista kandydatów `shipment` / `charge` (strona kupna jeszcze bez FV):

1. **Nasz numer** na fakturze — `shipment` / zlecenie podwykonawcy / `quotation` (to my je drukujemy na zleceniu dla przewoźnika i w mailu). Trafienie unikalne = pewność wysoka.
2. Kontener ISO, B/L, booking, PIN, nr SENT, płyta — jeśli jest w tekście/XML.
3. **KSeF / NIP** sprzedawcy = `party` + kwota brutto/netto (Decimal, ta sama waluta) + okno daty wokół rozładunku/wykonania vs otwarte `charge.buy` bez FV.
4. Wątek maila już dopięty do RFQ/zlecenia.
5. Relacja (POL/POD lub para krajów) + miesiąc — niska pewność.
6. Brak sygnałów → skrzynka **nieprzypisane**; filtr: ten sam przewoźnik, otwarte koszty, ±14 dni.

Progi (dane M-03): jedna kandydatura powyżej progu = podpowiedź „1-klik accept”; 2–8 = ranking do wyboru; zero albo remis = człowiek szuka. **Nigdy auto-podpięcie.**

Jedna FV na wiele zleceń (zbiorcza kosztowa): accept z podziałem linii → kilka powiązań; suma linii = kwota FV (SQL sprawdza, model nie sumuje).

**Faktury z innych kontynentów (brak NIP, brak naszego numeru, słabe tłumaczenie):**

- Nie zgadujemy zlecenia. Pokazujemy **krótką listę** (ten `party` / podobna nazwa, waluta, kwota w tolerancji, data, otwarty buy).
- Operator może: wybrać zlecenie · rozbić na kilka · zostawić w „nieprzypisane” · wysłać szkic maila „podaj numer zlecenia Omni / kontener” (`mail_draft`, HITL).
- **Profilaktyka (najważniejsza):** każde wychodzące zlecenie dla przewoźnika i każdy mail z Omni dostaje **twardy `shipment_ref`** (jeden format, kod + krótki URL). Im więcej FV wraca z tym numerem, tym mniej zgadywania.
- FA(3) pole `DodatkowyOpis` / referencje — mapujemy na ten sam ref, gdy polski podwykonawca wystawia nam KSeF.

Po accept: `purchase_invoice` + powiązanie ze zleceniem + `charge` (buy już jest albo człowiek wskazuje który). Potem sync FZ do ERP (§13l). Kwoty z draftu zatwierdzone przez człowieka, nie z LLM-a „na czysto”.

### 13n. Wydruki sieci drobnicowych + skan zwrotny na zlecenie (operator 2026-09-07)

Dla części sieci (paletówki UK/BE, Alliance/Palletforce/Palletline, krajowa drobnica SPEED) **brak etykiety albo CMR = ładunek nie wejdzie na linię**. To nie ozdoba — to warunek przyjęcia w hubie.

**Jak to robi Qargo (help, 2025–2026, nie kopia UI):**

- Szablony w konfiguracji: FV, list załadunkowy, wycena, CMR, trip sheet. Task `Generate document` / `Upload document`; override per klient.
- **Groupage CMR:** osobny CMR na każdą grupę dostaw w tripie (multi-drop). Lista towaru dłuższa niż kratka → automatyczna kopia CMR z ciągiem. Założenie: jeden origin załadunku.
- **Etykieta paletowa** po zapisie zlecenia (async); klient drukuje z portalu, żeby hub wiedział co zrobić przy podjęciu.
- **Etykieta sieciowa** (Palletforce / Alliance / Palletline): Zebra, wymiary 1:1, bez „Fit to page”. Generowana głównie na **eksport do sieci**; import = ręcznie w systemie sieci (Qargo tego nie zmyśla). Gdy nie jedzie Palletline — task „własne etykiety”.
- Powrót: Document Intelligence (OCR → match POD/CMR) + upload w apce / portalu.

**Jak to robi SPEED (dossier + strona drobnicy):**

- Własne wzory wydruków + dodatek Automation (desktop). CMR z danych zlecenia. Liczniki per lokalizacja.
- HBL/MBL + pule numerów master; LCL wchodzi w krajową sieć drobnicową (consol/deconsol).
- mSPEED LTL: skan kodu paczki/palety + zdjęcie POD; walidacja statusu.
- eSPEED: przewoźnik podpina skan POD; rozliczenie czeka na zwrot dokumentu.

**Omni — trzy warstwy (szablony = dane, nie T-SQL):**

| Warstwa | Co | Kiedy |
|---|---|---|
| 1. Katalog wymagań | `network_print_requirement`: sieć / `party_role` → jakie `document_kind` muszą być **wydrukowane** zanim wyjazd / przyjęcie w hubie | D9; blokada jak C8 (409), odblokowanie = wydruk + `source_ref` |
| 2. Silnik wydruku | `document_template` (layout, język, branding tenanta). Rodzaje: etykieta własna · etykieta sieci (SSCC, sort, hub, depot) · CMR · CMR groupage (per stop) · HBL/MBL (D6) · zlecenie przewoźnika · list załadunkowy | D9; U-print / PDF / ZPL na Zebra |
| 3. Skan zwrotny | ten sam plik wraca z magazynu, maila, apki, portalu | D2 + D9 + X3/X6 |

Na **każdym** naszym wydruku: czytelny `shipment_ref` + kod kreskowy / QR (`tenant` + `shipment` + `package` + `document_kind`). To ta sama profilaktyka co na FV (§13m).

**Podpięcie skanu — dwa tory (nie jeden „zawsze HITL / nigdy auto”):**

1. **Nasz kod odczytany** (skaner, kamera, QR z wydruku Omni) → SQL znajduje dokładnie jedno zlecenie/paczke → `shipment_document` zapisuje się od razu, z `source_ref=scan://…`. To skan magazynowy, nie ekstrakcja LLM. Zła trasa/status (wzorzec SPEED) = odrzut skanu, nie cichy zapis. Kolizja albo kod obcego tenanta = stop.
2. **Brak naszego kodu** (obcy CMR, sieć zagraniczna, rozmazany skan) → jakość zdjęcia (jak Photo POD) → klasyfikacja rodzaju → drabina jak §13m (numer, kontener, NIP, wątek, data) → **HITL accept**. Model nie zgaduje zlecenia.

Kanały: stanowisko skanera · załącznik maila · apka kierowcy · portal przewoźnika. Dedup: ten sam odcisk pliku + kind + shipment.

Po podpięciu: diff pól CMR/POD vs zlecenie (waga, sztuki, data) = X6, konflikty do recenzji, nie cichy overwrite. eCMR (TransFollow u Qargo) = C4, nie zastępuje papieru, dopóki prawo tego nie każe.

Etykieta **obcej sieci** (Palletforce itd.): tylko oficjalne API / plik z ich systemu po umowie (D8). Brak API = nasz szablon z polami, które sieć wymaga na papierze — nie udajemy ich generatora.

M-38 dziś to wskazanie bez bajtów. D9 dodaje bajty + szablon + wymóg sieci. Kwot na dokumencie nie ma — marża zostaje w `charge`.

### 13o. Jakość skanu (enhance + kadr) i recenzja split z ramkami (operator 2026-09-07)

Słabe zdjęcie z apki / maila / skanera nie idzie „na siłę” do modelu. Najpierw **gate + geometria**, potem Docling (już w M-20), potem człowiek w splitcie, który **już jest** (`hitl-review-split.tsx` + makieta `ui-04-hitl` + ADR-0003). Brakuje: preprocess, `bbox` na stronie, pewność **per pole**, edycja przed accept.

**Ten sam ekran** dla: zlecenie od klienta · FV kosztowa (§13m) · cennik / oferta od podwykonawcy, armatora, agenta · skan CMR/POD (§13n). Różni się `draft.kind`, nie nowym UI.

#### Pipeline (jeden, wszystkie kanały)

```
mail | załącznik | skan | apka kierowcy
  → quality gate
  → enhance + kadr (oryginał zostaje)
  → Docling layout/OCR (bbox + ocena strony)
  → instructor (pola, amount_text, span → bbox)
  → extraction_draft
  → split HITL (lewo dokument, prawo pola)
  → accept / reject / „zrób zdjęcie ponownie”
```

**Cel wizualny (operator 2026-09-07):** wynik ma wyglądać jak **skan z dobrego skanera płaskiego**, nie jak zdjęcie kartki w ręku. Biel papieru, równe światło, ostry druk, zero stołu / palców / trapezu. Oryginał zostaje; recenzja i OCR idą z wersji „skaner”.

**1. Silnik zdjęcia (apka / stanowisko) — jakość powstaje przy spuście, nie „w chmurze z rozmycia”.**

- Ramka strony na żywo; spust dopiero gdy prostokąt stoi i ostrość (Laplace) jest powyżej progu. Burst kilku klatek → zostaje najostrzejsza.
- Android: **ML Kit Document Scanner** (ten sam silnik co Dysk Google / Pixel) — detekcja krawędzi, auto-kadr, obrót, cienie. Tryb `BASE_WITH_FILTER` na FV/cennikach (crop + filtr, **bez** „wymaż plamy”). `FULL` (plamy, palce) tylko na POD/zdjęciu ładunku — na kwocie może zjeść pieczątkę albo cyfrę.
- iOS: **VisionKit** `VNDocumentCameraViewController` (systemowy skaner).
- Mail / upload z pulpitu: bez ML Kit → ten sam pipeline na serwerze.
- Za słabo = „zrób ponownie” w apce. Nie wysyłamy klatki, której nie da się wyprostować.

**2. Enhance „wygląd skanera” — OpenCV (`opencv-python-headless`), nie GAN.**

| Krok | Efekt skanera | Silnik |
|---|---|---|
| 4 rogi + `warpPerspective` | kartka na płasko, bez stołu | OpenCV |
| Deskew | linie poziome | minAreaRect |
| Spłaszczenie światła (tło / duży blur, dzielenie) | papier jednolity, bez cienia dłoni | OpenCV; Retinex/MSR jak w poradniku OpenCV |
| Punkt bieli | tło ≈ biały skaner, tusz zostaje | rozciągnięcie histogramu na kanale L |
| Tryb wyjścia | **kolor** (domyślnie FV — logo, pieczątka) · szary · B/W adaptacyjne (CMR) | filtr, nie nowy model |
| Unsharp na jasności | ostre glify | OpenCV |
| DPI | cel ~300 na stronę A4; jeśli za mało — **Lanczos**, nie generator | interpolacja |

Wyjście: JPEG/PNG wysokiej jakości albo PDF strony. Osobne `source_ref` oryginał vs skan. Lewy panel HITL pokazuje skan.

**Zakaz Real-ESRGAN / GFPGAN / inpainting „dopisz brakujący róg z tekstem”.** To nie skaner — to nowa treść. Docling: niski `ocr_grade` → lepsze zdjęcie albo inny OCR, nie GAN.

**P1:** odwijanie zmiętej kartki (PaddleOCR UVDoc) — A/B `ab_delta`, nie CI. Scanbot i inne SDK płatne = TO_VERIFY licencja, nie wymóg. Cloud DI tylko BYO (HC-05).

**3. Wyłapywanie danych — stack, który już wybraliśmy.**

- Docling (0.9): layout, tabele, OCR, **bbox klastrów**, od 2.34 oceny `layout` / `ocr` / `mean_grade` / `low_grade` (poor…excellent). `low_grade=poor` → ten sam komunikat co gate, albo recenzja z pomarańczowym banerem.
- Instructor: kandydaci z `amount_text` (Decimal w kodzie). Każde pole dostaje `bbox` (strona, x, y, w, h) + `confidence` 0–1 + `span_text`.
- Dziś w schemacie tego nie ma — X9 rozszerza `ExtractedChargeCandidate` / ogólny `ExtractedField` (rodzaj: stawka, NIP, numer FV, data, kontener, waga…). `unparsed_regions` zostaje.

#### Split recenzji (lewo / prawo)

Już narysowane w `docs/design/ui-04-hitl.canvas.tsx` i ADR-0003. Dziś split jest, **brak pewności per pole i zbiorczego odrzucenia z powodem**.

| Lewo | Prawo (po kliknięciu pozycji) |
|---|---|
| Cała strona (enhance), ramki na pola do importu; aktywna ramka = to, co wybrane | Co to jest (kod / etykieta) · wartość · waluta jeśli kwota · **pewność %** · `span_text` |
| Klik w ramkę zaznacza wiersz | Klik w wiersz podświetla ramkę |
| Strony wielostronicowego PDF | Edycja ręczna **przed** accept; oryginał z OCR zostaje; flaga `operator_override` (pewność modelu się nie „poprawia”) |

Pasma (dane M-03, nie magia): ≥0,85 zielone · 0,70–0,85 żółte · <0,70 pomarańcz + glif — **nie wchodzi w accept zbiorczy** bez osobnego kliknięcia (ui-04: próg 0,7, disambiguation, nie zgadywanie). Art. 50 na recenzji zostaje. Optimistic accept zakazany.

Kwot nie liczy JS ani model. Operator może poprawić `amount_text`; Decimal powstaje przy accept.

### 13p. Cyfrowa książka nadawcza — Poczta Polska (operator 2026-09-07)

Automatyzacja **ma sens** i jest oficjalna. Nie budujemy własnego „śledzenia z przeglądarki”. Dwa systemy PP, umowa biznesowa, sekrety tenanta (HC-05).

**Prawda w Omni:** tabela `postal_dispatch` (per tenant, RLS) — jeden wiersz = jedna przesyłka pocztowa. FK do `sales_invoice` (albo innego dokumentu wychodzącego) + `party`. `numer_nadania` = kod z nalepki. Zdarzenia i EPO to wiersze zależne z `source_ref`. PDF „Książka nadawcza” z PP to **artefakt**, nie jedyna księga.

**Zaznaczenie „faktura papierowa” = kanał Poczta Polska** (operator 2026-09-07).

Na `sales_invoice` pole kanału doręczenia (dane, nie osobny produkt): `electronic` (KSeF / mail / Peppol) albo `paper_post`. Zaznaczenie papieru **włącza** książkę nadawczą i druk. Nie wyłącza KSeF dla PL B2B — mandat 2026 zostaje; papier to kopia do koperty.

- Domyślnie z `party` (ten klient zawsze papier) — da się nadpisać na fakturze.
- `paper_post` bez wiersza `postal_dispatch` = faktura w kolejce „do nadania”, nie w stanie „wysłana”.
- Akcja „nadaj pocztą” / skan numeru jest widoczna tylko przy `paper_post`.
- Filtr książki = same papierowe. Raport: ile czeka na nalepkę.

#### Dwa oficjalne API (specyfikacje publiczne, IX 2026)

| System | Do czego | Kontrakt |
|---|---|---|
| **Elektroniczny Nadawca** SOAP WebAPI w96 (17.1, 2026-03-18) | Nadanie, nalepka, książka, EPO | `https://e-nadawca.api.poczta-polska.pl/websrv/` — stare `/websrv/` na e-nadawca.poczta-polska.pl do wyłączenia |
| **System śledzenia REST** | Statusy po numerze | `checkmailex` / `checkmailcollectionex` (drugie + `api_key` i uprawnienie). TLS ≥ 1.2 (NIS2/DORA) |

SOAP śledzenia (`tt.poczta-polska.pl`) zostaje zapasem; P0 = REST.

**Nadanie (EN), max 500 w pakiecie:** `clearEnvelope` → `addShipment` → `getPrintForParcel` (nalepka z kodem) → `sendEnvelope` → `getOutboxBook` (PDF książki + zestawienie nierejestrowanych). `numerNadania` wraca z EN albo nadajemy swój, gdy PP pozwoli.

**Nie „API albo numer” — numer jest kluczem, API jest rurą.** W książce zawsze stoi `numer_nadania` (kod z nalepki). Śledzenie i EPO pytają po tym numerze. Bez numeru nie ma wiersza.

**Jak numer wchodzi do Omni (kolejność od najlepszej):**

| # | Skąd numer | Kiedy | Wpisywanie |
|---|---|---|---|
| 1 | EN zwraca `numerNadania` przy `addShipment` | FV wychodzi z Omni („nadaj pocztą”) | **Zero ręcznego wpisu.** Nalepka z naszym wierszem. |
| 2 | Skan kodu z nalepki PP | Nadanie w okienku / już naklejona etykieta | Kursor w polu książki albo na otwartej FV → pisk skanera → numer + od razu `checkmailex` |
| 3 | Wklejenie / 13–20 znaków z walidacją | Awaria skanera, numer z maila PP | Enter; zły checksum = odrzut, nie cichy zapis |

Skaner w biurze: zwykły **USB/HID** (klawiatura — Datalogic, Honeywell, Zebra). Nie osobny sterownik, nie nowa apka. Kamera w apce / na stanowisku = zapas (ten sam silnik co QR zlecenia, §13n). Nie OCR-ujemy numeru z rozmazanego zdjęcia koperty, jeśli kod się nie czyta — wtedy pudełko 3.

Po skanie: jeśli jesteśmy na fakturze — wiersz książki wiąże się z nią. Jeśli na książce — lista „faktury tego kontrahenta bez nadania” (HITL, jeden klik). Ten sam numer dwa razy = ten sam wiersz (idempotencja).

EPO (imię) tylko jeśli przy nadaniu była usługa EPO — i tak po numerze, przez EN `getEPOStatus`.

#### Kto odebrał — tu jest haczyk

Śledzenie zwraca zdarzenia: `P_D` Doręczono, `P_UKEPO` „Udostępnienie podpisu odbiorcy”. **Imienia w REST nie ma.**

Imię i rola są w **EPO** (`getEPOStatus` w EN), typ doręczenia:

- `osobaOdbierajaca` — imię i nazwisko
- `podmiotDoreczenia` — m.in. ADRESAT, UPOWAZNIONY_PRACOWNIK, PELNOMOCNIK_ADRESATA, DOROSLY_DOMOWNIK, SASIAD, SKRYTKA_POCZTOWA…
- data doręczenia; opcjonalnie `withBioepo` = obraz podpisu (biometria tylko gdy urządzenie ją odda)

Wymaga **umowy EPO** i zaznaczenia usługi na przesyłce (`EPOSimpleType` / `EPOExtendedType`). Papierowe ZPO wraca kartką — wtedy skan (§13n/§13o) na fakturę, OCR nie zgaduje nazwiska jako faktu.

Karta EPO jest podpisana certyfikatem PP (aktualny do 2027-03-24; dwa XSD — obsłużyć oba). Podpisu i biometrii nie logujemy.

**Papierowe ZPO bez EPO:** w książce widać „nadana / w drodze / doręczona” ze śledzenia; „kto” = puste albo skan zwrotki po HITL.

#### Odświeżanie statusu

Wywołanie zewnętrzne **idempotentne** po `numer_nadania` + kodzie zdarzenia + czasie. Upsert zdarzeń, nie nowa historia przy każdym pollu.

Na start: przycisk „odśwież” na książce + odświeżenie przy otwarciu wiersza. Harmonogram (batch otwartych nadań) — gdy będzie realny job (X4), nie Temporal na siłę.

Zdarzenie kończące (`finished` / `zakonczonoObsluge`) zatrzymuje poll.

#### Prawo i zakres

`osobaOdbierajaca` to dane osoby — RLS tenanta, nie w promptach, nie w logach. B2C i tak odrzucone; tu zwykle pracownik firmy-adresata.

e-Doręczenia (skrzynka do urzędów) to **inny** kanał niż list PP — HZ, nie zastępuje książki nadawczej.

Kwot na wierszu pocztowym nie ma. Koszt znaczka = `charge` z `source_ref` (cennik PP albo faktura PP), nie z LLM.

### 13q. Luki PDF dociągnięte 2026-09-07

Źródło luk (42 nazwy): [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md). Werdykty twarde operatora. Nie 1:1 376 stron — każda **nazwana** funkcja ma wiersz tutaj **albo** w Rejestrze odrzuceń.

| Funkcja | Źródło | Status | Werdykt | Fala |
|---|---|---|---|---|
| **AI Margin Guard** — trip stratny; FSC poniżej rynku; oferta przewoźnika powyżej mediany; sugerowana cena sprzedaży | PDF s.23–24 | BRAK | ULEPSZ — warning SQL na `charge`; LLM nie liczy marży | HZ (P/V) |
| **Device Management BYO** — IMEI, provisioning, heartbeat, SIM tenanta (portal producenta Teltonika/Queclink) | PDF s.83–86 | BRAK | KOPIUJ — poświadczenia tenanta, nie nasz firmware | HZ TO_VERIFY |
| **Tender Radar** — TED Search API + eForms, nowe przetargi publiczne | PDF s.169 | BRAK | KOPIUJ | HZ; TO_VERIFY dostęp/licencja TED |
| **Operational Service Agent** — ticket: klasyfikacja → root cause → propozycja (np. przesuń slot) → HITL | PDF s.140–141 | BRAK | KOPIUJ ostrożnie — zawsze HITL; nie auto-zapis | HZ |
| **Blank sailing prediction** — predykcja odwołanego rejsu | PDF digest 3 / Ocean OS | BRAK | KOPIUJ | V/HZ (V3) |
| **IMO DCS / CII** — zużycie paliwa statków ≥5000 GT | PDF s.159–160, 348 | BRAK | KOPIUJ | HZ (morze); TO_VERIFY kto składa (armator vs spedytor) |
| **EU ETS + FuelEU Maritime** jako compliance | PDF s.159–160 | BRAK | KOPIUJ | HZ (morze); TO_VERIFY obowiązek tenanta |
| **Dispatch Agent** | PDF s.354 | BRAK | KOPIUJ — alias dyspozytora T6+V7, HITL; nie osobny produkt | HZ |
| **Cabotage Engine + RTPD** — licznik kabotażu; powrót kierowcy i pojazdu (dyrektywa 2020/1057) | PDF s.108–109, 328 | BRAK | KOPIUJ | C/V; TO_VERIFY prawo per kraj |
| **Combined Transport** — reżim prawny (nie nogi Huckepack) | PDF s.108, 328 | BRAK | KOPIUJ | C; TO_VERIFY |
| **ZSL / SENT-GEO / e-TOLL gateway (Level 2)** — Omni jako brama GPS → PUESC / e-TOLL | PDF s.257–259 | BRAK | KOPIUJ — taryfy publiczne lub umowa; nie zmyślaj kwoty | V/HZ; TO_VERIFY kto może być ZSL |
| **Biała lista jako bramka płatności** — NIP+rachunek przed przelewem, weryfikacja masowa | PDF s.256–257, 344 | CZĘŚĆ (M-10 lookup) | ULEPSZ — brama F przed `bank_payment`, nie drugi katalog | F (F4/C3) |
| **Sankcje: UBO + bank + HS/CN + port** | PDF s.183–184 | CZĘŚĆ (M-53) | ULEPSZ zakres wiersza M-53 (§8), nie nowy silos | C/V |
| **Knowledge Base** — trzecia warstwa chatu: Agent / Support / KB | PDF s.9–10 | BRAK | KOPIUJ — SOP/dokumentacja (HC-08); nie stawki/VAT | X/HZ |
| Nakładki map: **Parking, Fuel, Border, Ferries, Customs, Weather** | PDF s.20 | CZĘŚĆ (13k: ruch, LEZ, OpenRailwayMap) | ULEPSZ — katalog on/off, dane | V (§13k) |
| **Fuel Price Intelligence / rekomendacja stacji** — teraz vs następna stacja, €, km | PDF s.204–206 | BRAK | KOPIUJ | HZ; TO_VERIFY źródło cen stacji |
| **Topologie sieci drobnicowej** — hub&spoke, milk-run, wiele magazynów, wiele krajów | PDF s.130, 134–135; MC §23 | CZĘŚĆ (D1 linie+cutoff) | ULEPSZ — topologie jako dane planu | D1 / V |
| **Container Readiness Engine** | PDF s.285 | BRAK | KOPIUJ — po konektorze terminala | V/HZ |
| **Port Congestion Prediction** | PDF s.285, 292 | BRAK | KOPIUJ — wiersz V1 ledger | V/HZ |
| **Port Marketplace** — katalog Port→Terminal→Depot→Empty→Customs + capabilities/fees | PDF s.293 | BRAK | KOPIUJ — dane, nie giełda slotów | HZ |
| **Terminal Appointment & Gate OS** + dynamic reschedule | PDF s.291–292, 309–310 | BRAK | KOPIUJ — terminal API; bez gwarancji slotu (rejestr) | HZ |
| **Data licensing layer** — per dataset: source, license, geography, frequency, ToS | PDF s.368 | BRAK | KOPIUJ — tabela licencji źródeł (`source_ref` ≠ licencja) | HZ (ops/C) |
| **Omni Graph** — zdarzenie `ContainerETAChanged` → slot, truck ETA, magazyn, D&D, cash/revenue risk | PDF s.366–367 | BRAK | KOPIUJ — szyna na `entity_event` (B0); powiąż V6 | V (wieża) |
| **Network Design Optimizer** — lokalizacja hubów / struktura linii | MC §95E / §75 | BRAK | KOPIUJ — silnik OR, nie LLM | HZ |
| **Demand Engine** — popyt na lane | PDF s.172–176 | BRAK | KOPIUJ | HZ |
| **OMNI Market & Network Orchestrator** — giełdy+sieci+flota+magazyn+finansowanie jako źródła zdolności | PDF s.130 | BRAK | KOPIUJ ostrożnie HITL — parasol Make or Buy+D8, nie moduł „giełda” | HZ |
| **Macro & Geopolitical Intelligence** — warstwa sygnałów (energia, polityka, żegluga) | PDF s.165–172 | BRAK | KOPIUJ — korelacja ≠ przyczynowość | V/HZ (Market Intelligence) |
| **Ocean Email AI** — Customer RFQ → carrier RFQ → mail → parse → quote → HITL; pomiar response | PDF s.332–333 | BRAK | KOPIUJ — HITL | X/P (ocean) |
| **Logistics Autopilot** — dojrzałość 0–8 (pokazuje→…→wykonuje w granicach) | PDF s.252, 358 | BRAK | KOPIUJ jako reguła `/plan-modul` / DoD automatyzacji, nie osobny produkt | ops |
| **Lineage** — data lineage + model lineage + decision lineage | PDF s.367–368 | BRAK | KOPIUJ | V1/ops |
| **FerryGateway** — otwarty standard one-to-many | PDF s.67–68 | BRAK | KOPIUJ jako protokół promów | HZ; TO_VERIFY dostęp |
| **BYO kamera tenanta** — stream/incydent z kamery przewoźnika (np. Webfleet video) | PDF s.46–47, 53–55 | BRAK | KOPIUJ | HZ TO_VERIFY (prawo pracy / AI Act); nie scoring osoby |
| **TachoSync / zdalny odczyt DDD** | PDF s.83–86, 328 | BRAK | KOPIUJ po potwierdzeniu per model | V7 TO_VERIFY |
| **Border Crossing Intelligence** — warstwa ETA „BORDER” + nakładka | PDF s.20 | BRAK | KOPIUJ po źródle czasów odprawy | V2 + §13k; TO_VERIFY API |
| **Early Warning** poziomy GREEN/AMBER/RED/**BLACK** | PDF s.212–213, 350–351 | CZĘŚĆ (V6 bez nazwy/BLACK) | ULEPSZ — słownik statusów wieży | V6 |
| **e-Doręczenia** — skrzynka do urzędów (≠ książka nadawcza PP) | 13p / PDF | BRAK jako wiersz funkcji | KOPIUJ | HZ |

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
| Podsłuch / scraping komunikatorów giełd (Trans.eu, TIMOCOM, Teleroute, Transporeon) gdy nie jesteśmy stroną rozmowy | Art. 267 KK + RODO + ToS; brak publicznego API historii czatu (IX 2026). Wolno: własne wiadomości tenanta po oficjalnym API/eksporcie + metryki jobu spedytora + oficjalne ceny giełd (§13g) | ODRZUCONE na stałe (prawo) |
| Własne urządzenia GPS (projektowanie / produkcja / firmware) | Decyzja operatora 2026-09-07; HW = Teltonika + Queclink u przewoźnika, który chce pakiet Omni | ODRZUCONE na stałe (biznes) |
| Wymyślanie „SENT-ów" w krajach, które nie mają narodowego monitora ładunku | Fałszywa zgodność; katalog `monitoring_scheme` tylko ze źródłem prawnym (§13h) | ODRZUCONE na stałe |
| Scraping opinii słownych Trans.eu / TIMOCOM gdy brak endpointu | ToS + brak publicznego API komentarzy (IX 2026); scoring z partners-api jest oficjalny | ODRZUCONE na stałe |
| Niewidoczny piksel w ofercie bez zgody; tracker trzeciej strony; tracking osób prywatnych | ePrivacy / EDPB 2/2023 / PKE / CNIL 2026; B2C i tak odrzucone. Link do hostowanego PDF + zgoda na piksel = §13i | ODRZUCONE na stałe (prawo) |
| RAG/pgvector na logice wyceny, VAT, schemacie DB | HC-08: RAG wolno tylko na SOP/regulacjach/mailach/dokumentacji | ODRZUCONE na stałe (HC) |
| Deklarowanie „100% zgodności prawnej" / auto-reprezentacja celna bez upoważnienia | MC §18/§53: architektura pod zgodność ≠ gwarancja prawna; przedstawiciel celny wymaga umocowania | ODRZUCONE na stałe |
| „AI przewiduje przyszłość" jako obietnica marketingowa | MC §9/§99: komunikujemy zmierzoną skuteczność (Prediction Ledger), nie magię | ODRZUCONE na stałe |
| Dwa osobne produkty (Super TMS + system dla korporacji) | PDF s.254: jeden Omni Core, dwie perspektywy (Operator / Enterprise) | ODRZUCONE na stałe (architektura) |
| 200 niezależnych silosów-modułów | PDF s.2, 36, 129: silniki + wspólny model; katalog §92 zostaje jako nazwy powierzchni | ODRZUCONY mechanizm |
| Plik „MASTER BLUEPRINT / Cursor rules” z końca PDF | ChatGPT go **nie wygenerował** (s.375); kanon = AGENTS + GROUNDING + ta matryca | ODRZUCONE (artefakt nieistniejący) |
| SLA marketingowe „oferta w 8 minut”, „wdrożenie w 4 h” | MC §2: copy mockupu, nie wynik produkcyjny | ODRZUCONE jako gwarancja |
| HERE jako baza map/telematyki | PDF s.66: licencja asset-management; hybryda OSM/NAP + płatne premium | ODRZUCONE jako podstawa |
| Produkcyjne kafelki z `tile.openstreetmap.org` | Polityka OSMF: serwer społecznościowy nie jest CDN dla aplikacji; darmowe podkłady = OpenFreeMap / Geoportal / self-host (§13k) | ODRZUCONE na stałe |
| Sumowanie nakładających się oszczędności z tabel PDF (tender+procurement+wieża) | PDF s.238: nakładają się; nie dodawać dwa razy | ODRZUCONE jako metryka sprzedażowa |
| Auto-zlecenie / auto-`charge` z maila albo z geofence bez HITL | HC-04 + PDF s.51–53: propozycja tak, zapis po człowieku | ODRZUCONE na stałe |
| Auto-podpięcie FV kosztowej pod zlecenie bez accept | Ten sam kontrakt co stawki; za granicą za mało pól na pewność (§13m) | ODRZUCONE na stałe |
| Auto-podpięcie skanu dokumentu bez naszego kodu i bez HITL | Obcy CMR/etykieta sieciowa nie daje pewności; bez QR Omni zostaje drabina + accept (§13n) | ODRZUCONE na stałe |
| Procedury T-SQL / dodatek Automation jako silnik wydruków (mechanizm SPEED) | Ten sam anty-wzorzec co cenniki; szablon = dane (D9) | ODRZUCONY mechanizm, funkcja wchodzi |
| Udawanie generatora etykiet Palletforce/Alliance bez ich API | Qargo sam odsyła import do systemu sieci; my też (§13n, D8) | ODRZUCONE na stałe |
| Real-ESRGAN / GFPGAN / inny GAN-upscale na FV, CMR, cenniku | Dopowiada glify; kwota nie może powstać z wymyślonej cyfry (§13o) | ODRZUCONE na stałe |
| Accept HITL bo „pewność wysoka”, bez kliknięcia człowieka | ADR-0003 + HC-04; pewność tylko sortuje recenzję | ODRZUCONE na stałe |
| Scraping strony śledzenia PP / Envelo zamiast REST/EN | ToS + NIS2; jest oficjalne API (§13p) | ODRZUCONE na stałe |
| Obietnica „kto odebrał” przy samym papierowym ZPO, bez EPO i bez skanu zwrotki | Śledzenie nie oddaje imienia; imię = `getEPOStatus` albo HITL ze skanu (§13p) | ODRZUCONE jako gwarancja |
| Logowanie podpisu / biometrii EPO | RODO; karta zostaje w storage tenanta, nie w logach | ODRZUCONE na stałe |
| Surowy SQL / login sa do bazy Comarch/Subiekt/Symfonia | Omija Sferę/CDN/WebAPI, psuje gwarancję i RLS po ich stronie | ODRZUCONE na stałe |
| Podwójne wysłanie tej samej FV do KSeF (Omni i ERP) | Decyzja 2026-09-07: wystawia wyłącznie Omni; ERP tylko odbiera dokument | ODRZUCONE na stałe |
| ERP nadpisujący kwoty `charge` / druga tabela marży | HC-03 | ODRZUCONE na stałe |
| **Driver Score** (Safety/Fuel/Smoothness i analogiczne scoringi kierowcy-osoby) | AI Act + RODO art. 22; analogia auto-scoringu JDG. KPI pojazdu/tripa zostają w SQL | ODRZUCONE na stałe (prawo) |
| **Driver Profitability** — revenue/fuel/accident cost na osobę | Ten sam zakaz scoringu osoby; koszt tripa/pojazdu zostaje na `charge` | ODRZUCONE na stałe (prawo) |
| Własny produkt **Video AI / DMS / ADAS / OmniVision** (kamery, zmęczenie, telefon jako produkt Omni) | Jak własny HW GPS: zero własnego produktu wideo. BYO kamera tenanta = HZ TO_VERIFY (§13q) | ODRZUCONE na stałe (biznes) |
| **Device Management / FOTA własnego firmware** (IMEI/OTA naszego stosu) | Operator: zero własnego HW; FOTA Omni nie powstaje. BYO portal producenta = HZ TO_VERIFY (§13q) | ODRZUCONE na stałe (biznes) |
| **VAT OSS / IOSS** | B2C już poza produktem; B2B OSS nie jest jobem tenanta spedycyjnego | ODRZUCONE na stałe (biznes) |
| **Benchmarki między tenantami** z danych poufnych bez zgody/umowy | HC-01 + MC §93 zasada 5; Market Intelligence tylko dane licencjonowane / własne | ODRZUCONE na stałe |
| **Selenium / automatyzacja logowania** do portalu terminala; obejście zabezpieczeń | PDF s.309, 296: zakaz. Portal-only = zadanie człowiekowi, nie bot. Integration Hub „portal-fallback” ≠ Selenium | ODRZUCONE na stałe |
| Gwarancja **„zawsze zarezerwujemy slot”** | PDF s.290: capability matrix, CargoCard, brak API. Gate OS = HZ po API (§13q); obietnica = kłamstwo | ODRZUCONE jako gwarancja |
| **JPK jako moduł Omni** | Prawda JPK w ERP/FK; adapter nie liczy (§13l). Nie osobny silnik fiskalny w Omni | ODRZUCONE na stałe |
| **Scoring osoby z wideo** (zmęczenie/telefon/ADAS jako ocena pracownika, także na BYO streamie) | AI Act + art. 22; BYO ingest incydentu ≠ ocena osoby | ODRZUCONE na stałe (prawo) |

## Przewaga nad Qargo i SPEED (cel: lider)

1. **Wieża z łańcuchem skutków** — visibility → prediction → impact → decision → execution; klient korporacyjny widzi, co się stanie z magazynem/produkcją/sprzedażą/EBITDA, **jeśli nie zareaguje**. Potwierdzone jako wolna pozycja (Qargo road-first bez shipperów; SPEED bez predykcji).
2. **Prediction Ledger** — każda predykcja mierzona po fakcie (MAE/kalibracja/coverage); dowód jakości zamiast „AI przewiduje".
3. **Multimodal + finanse + celny + faktoring w jednym modelu danych** z RLS — łańcuch wycena → zlecenie → faktura → bank → NBP → rozliczenia już działa.
4. **AI z HITL i audytem** (AI Act minimal risk) — ekstrakcja → wycena → zlecenie w produkcie; reguły i podsumowania dojdą jako dane + HITL, nigdy autonomiczny zapis.
5. **Web-native multi-tenant od dnia 1** — iSPEED dopiero startuje; Qargo web, ale bez PL-compliance (KSeF/SENT/biała lista). Czas-do-wartości i konfiguracja jako dane = kontra na największy ból wdrożeń SPEED.

## Świadome POMIŃ (funkcja ≠ mechanizm)

Stack Qargo (Django/GraphQL/Apollo/Ant/Linaria) · konfiguracja przez ręczne procedury T-SQL · polskie nazwy kolumn w bazie · branding/kod/assety obu systemów · WhatsApp (teraz) · drugi grid engine.
