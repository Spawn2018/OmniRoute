# Inwentarz MC + PDF — audyt „wszystko w matrycy albo odrzucone”

**Po co:** operator słusznie zakwestionował §13e („103 sekcje 1:1”). To był audyt **nagłówków** master-contextu, nie każdej funkcji z PDF (376 s. / ~17,5k linii). Ten plik jest checklistą ziarna funkcji.

**Źródła:** `D:\Downloads\OmniRoute_Chronologia_Ustalenia_Master_Context.md` (§0–103 + katalog §92) · digesty `chatgpt-pdf-digest-1/2/3.md` · matryca [benchmark-tms-2026.md](benchmark-tms-2026.md) · rejestr odrzuceń tamże.

**Ziarno:** nazwana funkcja / silnik. Pola (CMR, kontener, dock…) wchodzą do kart przy `/plan-modul` (ADR-0004) — nie dublujemy tu 400 kolumn.  
**2026-09-07:** 42 nazwy z [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md) są w matrycy §13q albo w rejestrze odrzuceń — to nie jest inwentarz 1:1 376 stron.

**Legenda:** MAT = wiersz w matrycy §… · ODR = rejestr odrzuceń · ZAS = już w AGENTS/HC/ADR (nie osobny feature).

## A. Master-context §0–103

| § | Temat | Werdykt |
|---|---|---|
| 0 | Super TMS + wieża + telematyka + finanse + twiny | MAT wnioski / §12 |
| 1 | Platforma multimodalna, jakość kodu, Cursor | ZAS AGENTS |
| 2 | WWW / „oferta w 8 min” / cennik | ODR (marketing, nie SLA) |
| 3 | Qargo jako inspiracja, nie kopia | ADR-0004 |
| 4 | Teltonika + Queclink | MAT §13g |
| 5 | Chłodnie / temperatura | MAT §9 HZ |
| 6 | Diagnostyka pojazdu | MAT §13c HZ |
| 7 | Telematyka jako biznes | MAT §12 HZ + ODR własny HW |
| 8 | Routing, live + historyczny traffic | MAT §13d |
| 9 | Naukowe predykcje | MAT §9 V1 |
| 10 | ETA + czas pracy | MAT §13j (dwa ETA) + V2/V7 |
| 11 | Promy | MAT §13j FERRY_REST + watchdog |
| 12 | Floating trailers | MAT §13c T2 |
| 13 | Dwóch kierowców | MAT §13c V7 |
| 14 | Tachograf | MAT V7 + §13j solver |
| 15 | Wirtualny doradca transportowy | MAT §13e HZ |
| 16 | Biuro czasu pracy | MAT §13e V7→HZ |
| 17 | ADR | MAT §8 / §13e |
| 18 | Prawo EU/świat | MAT §13e + ODR „100% zgodności” |
| 19 | Pakiet Mobilności / płace | MAT V7 F5 |
| 20 | Koszt zlecenia vs zasobu | MAT §13j Cost Allocation |
| 21 | Auto plan ładunku/pojazdu | MAT §13e V/HZ |
| 22 | VRP 1000+ | MAT §13e V/HZ |
| 23 | Drobnica topologie | MAT Fala D |
| 24 | Sieci zewnętrzne first/last mile | MAT D8 |
| 25 | Magazyn | MAT D3; WMS pełny HZ |
| 26 | Skanery / etykiety | MAT D2 + §13j Label |
| 27 | Harmonogram linii | MAT D1 + §13j Linehaul |
| 28 | Cenniki drobnicowe | MAT D5 |
| 29 | Giełdy | MAT §13g |
| 30 | Rynek stawek | MAT P / HZ market data |
| 31 | Pricing Engine | MAT Fala P |
| 32 | Czytanie maili | MAT M-20 + §10 |
| 33 | Cyfrowy bliźniak | MAT B0 / §12 |
| 34 | Bliźniak spedytora | MAT §12 Email Twin |
| 35 | CRM | MAT §13c X/HZ |
| 36 | Portal klienta | MAT X1 |
| 37 | Portal przewoźnika | MAT X2 |
| 38 | Faktoring | MAT F7 |
| 39 | Bankowość | MAT F4 + §13j adapter |
| 40 | Faktury / KSeF | MAT F1 |
| 41 | Wywiadownie | MAT §13a |
| 42 | Cyfrowy CFO | MAT M-15 + §12 |
| 43 | Prognoza cen | MAT §13e V/HZ |
| 44 | Palety | MAT D7 |
| 45 | Przetargi | MAT §13f |
| 46 | Predykcje audytowalne | MAT V1 |
| 47 | Morze FCL/LCL | MAT T3 D6 |
| 48 | Maritime pricing | MAT P4 |
| 49 | D&D / dopłaty | MAT V3 P4 |
| 50 | ETD/ETA/rollover | MAT V3 |
| 51 | Intermodal | MAT nogi M-48… + D |
| 52 | Sankcje | MAT M-53 |
| 53 | Wirtualna agencja celna | MAT C + ODR auto-reprezentacja |
| 54 | Porty / terminale EU | MAT HZ konektory |
| 55 | Gdańsk / Gdynia | MAT HZ Baltic Hub P0 |
| 56 | Corporate Watchtower | MAT V6 |
| 57 | Live + predictive visibility | MAT V |
| 58 | Stock / produkcja / sprzedaż | MAT V6 |
| 59 | Pogoda | MAT §13h (cała Europa) |
| 60 | Wysokość trasy | MAT §13j |
| 61 | Paliwo | MAT B0 + §13j anomalia + karty HZ |
| 62 | Reklamacje | MAT M-55 + §13j Claims OS |
| 63 | Support IT ≠ status ładunku | MAT §12 chat vs portal |
| 64 | Carbon | MAT C5 + §13j warstwy |
| 65 | Import obcych zleceń | MAT §13e + §13j Terms AI |
| 66 | Szablony dokumentów | MAT §11 |
| 67 | Custom workloads | MAT §13c T5→HZ |
| 68 | Archiwum klientów / NBP | MAT §13e |
| 69 | Integracja armatorów | MAT HZ |
| 70 | Auto wystawienie na giełdę | MAT §13e HZ |
| 71 | Tracking morski / anomalie | MAT V |
| 72 | Przetargi korporacyjne | MAT §13f |
| 73 | Wieża: vis→pred→impact→dec→exec | MAT V6 |
| 74 | Wybór źródła transportu | MAT §13j Make or Buy |
| 75 | Optymalizacja sieci | MAT §13e V/HZ |
| 76 | Green zones / restrykcje | MAT §13d |
| 77 | Myto | MAT §13h |
| 78 | Koszt kierowcy/floty | MAT §13e |
| 79 | Customer pricing | MAT P |
| 80 | Corporate procurement | MAT §12 HZ |
| 81 | AI | ZAS HC-02 |
| 82 | AI + HITL | ZAS HC-04 |
| 83 | Twin jako warstwa | MAT B0 |
| 84 | Compliance architecture | MAT §13e |
| 85 | Źródła danych (internal/external) | ZAS + katalog konektorów przy umowie |
| 86 | Data provenance | ZAS `source_ref` |
| 87 | Prognoza probabilistyczna | MAT V1 |
| 88 | Prediction performance | MAT V1 + §13j karty |
| 89 | Statystyki / raporty | MAT §12 generator |
| 90 | Bezpieczeństwo | ZAS HC + S59 park |
| 91 | SQL / architektura danych | ZAS CP-03, ADR-0004 |
| 92 | Katalog 120 nazw | sekcja B niżej |
| 93 | Zasady 1–7 (nie wymyślać API/prawa…) | ZAS AGENTS + ODR |
| 94 | Architektura logiczna | ADR-0004 + §12 |
| 95 | Silniki A–L | MAT §12 (Integration…Compliance) |
| 96 | Fazy 1–7 rozwoju | [kolejka-propozycja.md](kolejka-propozycja.md) |
| 97 | Fakt vs plan | ZAS honesty / CURRENT |
| 98 | Instrukcja dla agenta | ZAS AGENTS |
| 99 | Przewaga: zmierzona skuteczność | MAT wnioski |
| 100 | Logistics OS | MAT wnioski |
| 101 | Instrukcja kolejnej analizy | ten plik |
| 102 | Brak stenogramu 1:1 rozmowy | uczciwość MC; PDF jest źródłem funkcji |
| 103 | Zasada końcowa | ZAS |

## B. Katalog MC §92 (120 nazw)

Wszystkie są albo falą / M-xx, albo HZ, albo ODR. Nie budujemy 120 silosów (ODR).

| # | Nazwa | Gdzie |
|---|---|---|
| 1 | Dashboard | UI Shell / wieża S32 |
| 2 | CRM | §13c X/HZ |
| 3–6 | Road TMS / FTL / LTL / Groupage | Fala T+D |
| 7 | Network planning | D1 + V |
| 8–10 | Fleet / Drivers / Trailers | T2 |
| 11–12 | Floating trailers / two-driver | §13c |
| 13–15 | Telematics / Teltonika / Queclink | §13g |
| 16–18 | Refrigeration / temp / diagnostics | §9 HZ |
| 19–22 | Tacho / hours / compliance / ADR | V7 C |
| 23–29 | Maritime FCL/LCL/consol/carriers/coloaders/agents/trucking | T3 D6 P4 HZ |
| 30–34 | Ports / terminals / slot / AIS / vessel | HZ + V4 |
| 35–39 | Rail / China rail / air / intermodal / huckepack | M-48… + HZ air |
| 40–43 | Customs / bonded / recognized place / sanctions | Fala C + M-53 |
| 44–48 | Warehouse / cross-dock / labels / scanners / inventory | D3 D2 D9; §13n; WMS HZ |
| 49–50 | Linehaul / timetables | D1 |
| 51–58 | Pricing / rate / FSC / toll / market / hist / spot / contract | P + §13h |
| 59–60 | Prediction / ledger | V1 B0 |
| 61–68 | Traffic / hist traffic / weather / elevation / restrictions / LEZ / ferry / ETA | §13d §13h §13j |
| 69–71 | Disruption / claims / damage | V8 HZ + §13j |
| 72–76 | Documents / OCR / email AI / copilot / tender AI | M-20 §10 §13f §13m §13n |
| 77–83 | CFO / twins / watchtower / SC risk / inventory / production / sales | §12 V6 |
| 84–88 | Portals / driver app / customer chat / tech support | X + §12 |
| 89–101 | Banking / factoring / fuel cards/tanks / billing / KSeF / VAT / VAT-EU / whitelist / SENT / NBP / credit / controlling | F C + §13h SENT-EU |
| 102–103 | Carbon / reporting | C5 + §13j |
| 104–109 | Tender / procurement / ext networks / exchanges / sourcing / contracts | §13f D8 §13g HZ |
| 110–115 | API hub / integration / workflow / rules / custom workloads / audit | §13e T5 M-71 |
| 116–120 | Security / regulatory knowledge / customer support / incidents / observability | HC + S59 + M-37 |

## C. PDF — funkcje, które ginęły w nagłówku (teraz §13j)

Cost Allocation · Make or Buy · TIME-TO-FIX · dwa ETA · FERRY_REST · ferry watchdog · Driver Time Solver · Legal Feasibility · Time Simulation · geofence waiting HITL · karta drogowa · fuel anomaly · elevation · Claims OS + słownik szkód · VAT Engine · Terms AI · Response Intelligence · Linehaul what-if · Consolidation Engine · Opportunity / Transformation Office · spend leakage · Operator vs Enterprise · bliźniak urzędu · Carbon data≠raport · model/data/prediction cards · Unified Telemetry · cache tras · akceptacja z maila HITL · P&O API · marża na promie · zakaz „poprawiania” tacho · 6 pytań przy module · słownik naczep/osi · Label Engine · dock window pola · Bank Adapter · credit warning · Photo POD quality · FSC per usługa · Connected Carrier (HZ).

## D. PDF — świadomie nie w produkcie (rejestr)

Stack Django/GraphQL/Ant · T-SQL SPEED · kopia assetów · auto-score JDG/osób · B2C · BIK · WhatsApp (odz.) · Energy (odz.) · mikroserwisy/Temporal przed warunkiem · landing/SLA 8 min · wycena spółki/GMV · scraping · RAG na wycenie · „100% prawa” · „AI wróży” · własny firmware · fałszywe SENT-y · piksel bez zgody · dwa produkty · 200 silosów · nieistniejący blueprint · HERE jako baza · suma nakładających się oszczędności · auto-zapis z maila/geofence.

## E. Czego ten plik nadal nie jest

Nie jest kartą 400 pól z digestu §3 (cargo wymiary, Local Charge Library, reefer setpoint…). To idzie przy Planie konkretnej pozycji. Nie jest stenogramem 376 stron — PDF zostaje w `docs/_source/benchmark/` / katalogu digestów.
