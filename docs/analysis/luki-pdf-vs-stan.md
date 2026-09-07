# Luki PDF/MC vs stan-planu

**Data:** 2026-09-07 · **Nie kanon.** Nie edytuje [stan-planu-funkcje.md](stan-planu-funkcje.md). Nie commit.

**Werdykt:** stan-planu **nie** pokrywa 376 stron PDF 1:1. Ma **47** wierszy „zaplanowane w 100%” plus tabele 2–4 (25+37+35 = 97) = **144** wiersze. To jest wycinek: rozmowa operatora + **36/36** z §13q + **10/10** odrzuceń PDF. Reszta matrycy (§12, §13j, §13c/e/f, kawałki §2–11) siedzi w [benchmark-tms-2026.md](benchmark-tms-2026.md) i **nie** ma wiersza w MD.

MC **103** nagłówki + katalog **120** to nie 223 silniki. Inwentarz mapuje nagłówki i etykiety powierzchni — grubo. Pola (324) i konektory per marka nie są ziarnem.

## Liczby

| | n |
|---|---|
| Nazwy z PDF/MC **bez wiersza** w stan-planu, **są** w matrycy / §13q / rejestrze | **136** |
| w tym blisko synonimu w innym wierszu MD (CZĘŚĆ — i tak brak nazwy) | 28 |
| Nazwane silniki z ziarna audytu 42 **nigdzie** (ani MD, ani matryca, ani rejestr) | **0** |
| Residua poza ziarnem (nie liczone jako „nigdzie”) | pola ~324; konektory per marka; SKU OmniTrack/OmniCFO; GMV; nieistniejący blueprint |

§13q **36/36** i **10** odrzuceń PDF **są** w stan-planu (tabele 2–4). Luka MD ≠ luka matrycy.

## Metoda

Ziarno = **nazwa** silnika/funkcji z PDF, MC §95 albo wiersza matrycy. Jak w [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md): kawałki rozrzucone po falach **nie** zaliczają nazwy. „W stan-planu?” = wiersz w jednej z czterech tabel (nie zdanie HZ po §4). Alias z audytu B nie inflacjuje „nigdzie”.

Akcja:

- **już w matrycy tylko nie w MD** — jest wiersz w §1–13q albo rejestrze; brak wiersza w stan-planu.
- **dopisać do stan-planu** — nie używane: zero silników poza matrycą.
- **odrzucone** — rejestr / tabela 4; tu tylko gdy nazwa PDF nie ma wiersza w MD (reszta odrzuceń PDF już jest w §4).

---

## 1. Już w stan-planu (nie luka MD)

| Co | Gdzie w MD |
|---|---|
| 47 zaplanowanych (M10, B0, T–V bez D8/F5/F7/C2/V7) | tabela 1 |
| 36 wierszy §13q | tabele 2 i 3 |
| 10 odrzuceń PDF (Driver Score, Video AI, FOTA własny, VAT OSS, benchmarki tenantów, Selenium, gwarancja slotu, JPK, scoring z wideo, Driver Profitability) | tabela 4 |
| D8, F5, F7, C2, V7, Auth0, S21, … | tabela 3 |
| WhatsApp, Energy Intelligence, Connected Carrier, twiny pełne, war room, autonomous negotiation | **tylko proza** po §4 — **nie** wiersz; powtórzone niżej jako brak wiersza |

---

## 2. W matrycy, brak wiersza w stan-planu

Kolumna „W stan-planu?” = **NIE**, chyba że CZĘŚĆ (inna nazwa w wierszu, nie ta).

### 2a. §12 — silniki C-level (24)

What-if = V8 w tabeli 1. Pozostałe 24 z 25 wierszy §12:

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Digital twin „do wszystkiego” (warstwa twinów) | NIE (B0 = ledger, nie twin) | TAK §12 | już w matrycy tylko nie w MD |
| Omni Network Digital Twin | NIE (proza „twiny pełne”) | TAK §12 | już w matrycy tylko nie w MD |
| Business Impact Graph (SKU→EBITDA) | NIE (wzmianka przy Omni Graph) | TAK §12 | już w matrycy tylko nie w MD |
| Revenue at Risk + Working Capital Engine | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Disruption War Room | NIE (proza HZ) | TAK §12 / §9 | już w matrycy tylko nie w MD |
| Procurement Autopilot | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Contract Intelligence | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Regulatory Radar | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Counterparty Risk Engine | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Fraud & Anomaly Engine | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Multi-Objective Optimizer | NIE (Network Design ≠ wagi na istniejącej sieci) | TAK §12 | już w matrycy tylko nie w MD |
| Autonomous Negotiation Engine | NIE (proza HZ) | TAK §12 | już w matrycy tylko nie w MD |
| Memory Graph | NIE (wzmianka przy Omni Graph) | TAK §12 | już w matrycy tylko nie w MD |
| Decision Ledger | NIE (Lineage mówi „wycinek”) | TAK §12 / §11 | już w matrycy tylko nie w MD |
| Executive AI (pytania zarządu) | NIE (Early Warning ≠ ten job) | TAK §12 | już w matrycy tylko nie w MD |
| Energy Intelligence | NIE (proza HZ) | TAK §12; ODROCZONE rejestr | już w matrycy tylko nie w MD |
| Customer Chat | NIE (X1 = portal, nie chat) | TAK §12 | już w matrycy tylko nie w MD |
| IT Support Agent | NIE (wzmianka przy Operational Service Agent) | TAK §12 | już w matrycy tylko nie w MD |
| Email Digital Twin | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Slot Intelligence + Secure Chain + Port Identity | NIE (Readiness ≠ Slot) | TAK §12 | już w matrycy tylko nie w MD |
| Omni Market Intelligence | NIE (Macro geo ≠ produkt danych) | TAK §12 | już w matrycy tylko nie w MD |
| Telematyka jako biznes / 5 modeli / Connected Carrier | NIE (proza HZ) | TAK §12 / §13j | już w matrycy tylko nie w MD |
| Generator raportów (LLM po SQL) | NIE | TAK §12 | już w matrycy tylko nie w MD |
| Widoki per rola (FTL ≠ drobnica ≠ morze) | NIE (T6 = cztery widoki boardu) | TAK §12 | już w matrycy tylko nie w MD |

### 2b. §13j — nazwy, które ginęły w silniku nadrzędnym (35)

Photo POD jest w X9. Prom-marża = mechanizm `charge`. Apka≠tacho = V7. Sześć pytań = ops, nie silnik. Connected Carrier = 2a.

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Cost Allocation Engine | NIE (T4 = widok SQL na `charge`) | TAK §13j | już w matrycy tylko nie w MD |
| Make or Buy | NIE (wzmianka przy Orchestrator) | TAK §13j | już w matrycy tylko nie w MD |
| TIME-TO-FIX | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Dwa ETA: fizyczne vs prawne | NIE (V2 = planned/historical/live/risk) | TAK §13j | już w matrycy tylko nie w MD |
| `FERRY_REST_EVENT` | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Ferry watchdog | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Driver Time Solver | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Legal Feasibility Check | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Compliance & Time Simulation | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Geofence → waiting (HITL) | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Elektroniczna karta drogowa | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Fuel fraud / anomalia paliwa | NIE (wzmianka przy Fuel Price Intelligence) | TAK §13j | już w matrycy tylko nie w MD |
| Profil wysokości | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Claims OS + Deadline Engine + słownik szkód | NIE | TAK §13j / §13e | już w matrycy tylko nie w MD |
| VAT Engine | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Terms AI | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Response Intelligence | CZĘŚĆ X7 (13j: ULEPSZ) | TAK §13j | już w matrycy tylko nie w MD |
| Linehaul Schedule Engine | CZĘŚĆ D1 (13j: ULEPSZ) | TAK §13j | już w matrycy tylko nie w MD |
| Consolidation Engine | CZĘŚĆ D6 (13j: ULEPSZ) | TAK §13j | już w matrycy tylko nie w MD |
| Opportunity Engine | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Transformation Office | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Spend leakage | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Bliźniak urzędu | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Carbon Data Layer ≠ raport ESG | CZĘŚĆ C5 | TAK §13j | już w matrycy tylko nie w MD |
| Karty naukowe (model/data/prediction card) | CZĘŚĆ V1 | TAK §13j | już w matrycy tylko nie w MD |
| Unified Telemetry Model | CZĘŚĆ V5 `PositionEvent` | TAK §13j | już w matrycy tylko nie w MD |
| Cache tras | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Akceptacja oferty z języka maila (HITL) | NIE | TAK §13j | już w matrycy tylko nie w MD |
| Słownik naczep + dane osiowe | CZĘŚĆ T2/pola | TAK §13j | już w matrycy tylko nie w MD |
| Label Engine | CZĘŚĆ D9 | TAK §13j | już w matrycy tylko nie w MD |
| Dock time window | CZĘŚĆ D3 | TAK §13j | już w matrycy tylko nie w MD |
| Bank Adapter Layer | CZĘŚĆ F4 | TAK §13j | już w matrycy tylko nie w MD |
| Credit warning przy limicie | CZĘŚĆ F6 | TAK §13j | już w matrycy tylko nie w MD |
| FSC per usługa | CZĘŚĆ P3 | TAK §13j | już w matrycy tylko nie w MD |
| P&O Freight API (nazwa) | CZĘŚĆ B#23 | TAK §13j | już w matrycy tylko nie w MD |

### 2c. §13c — katalog §92 (18)

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| CRM | NIE | TAK §13c | już w matrycy tylko nie w MD |
| AIR OS | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Floating trailers | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Multi-manning | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Diagnostyka pojazdu / predictive maintenance | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Huckepack / wagony kieszeniowe | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Magazyn celny + miejsce uznane | NIE | TAK §13c | już w matrycy tylko nie w MD |
| WMS pełny | NIE (D3: „nie pełny WMS”) | TAK §13c | już w matrycy tylko nie w MD |
| Traffic live + historyczny | CZĘŚĆ V2 | TAK §13c / §13d | już w matrycy tylko nie w MD |
| Karty paliwowe + zbiorniki | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Spot vs contract + historia rynkowa | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Tender management / Tender AI (SIWZ) | NIE (Tender Radar = TED; P6 = ważność oferty) | TAK §13c / §13f | już w matrycy tylko nie w MD |
| Contract management | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Financial controlling | CZĘŚĆ F3 | TAK §13c | już w matrycy tylko nie w MD |
| Workflow / custom workloads admina | CZĘŚĆ T5 | TAK §13c | już w matrycy tylko nie w MD |
| Incident management | NIE | TAK §13c | już w matrycy tylko nie w MD |
| Import zleceń obcych spedycji | CZĘŚĆ X9/M-20 | TAK §13c | już w matrycy tylko nie w MD |
| LEZ / green zones jako silnik danych | CZĘŚĆ nakładki T6/§13k | TAK §13c / §13d | już w matrycy tylko nie w MD |

### 2d. §13e (19)

C8 blokada dokumentów jest w C1+C7+C8.

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Compliance / Legal Engine | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Agenci Transport / ADR / Customs / Legal Advisor | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Wirtualne biuro / Tacho Office | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Remuneration engine | CZĘŚĆ F5 (diety; 13e szersze) | TAK §13e | już w matrycy tylko nie w MD |
| Network / resource costing | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Fleet cost model | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Loading optimizer + VRP 1000+ | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Ubezpieczenie cargo per zlecenie | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Gospodarka oponami / serwis | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Import / migracja SID | NIE | TAK §13e | już w matrycy tylko nie w MD |
| SMS / e-mail outbound (bramki) | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Dock scheduler | CZĘŚĆ D3 | TAK §13e | już w matrycy tylko nie w MD |
| Sandbox / demo per tenant | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Widok brakujących kosztów (Trips to Bill) | CZĘŚĆ P5 | TAK §13e | już w matrycy tylko nie w MD |
| Fiscal risk scoring podmiotu | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Auto-wystawienie na giełdę | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Integration Hub | NIE | TAK §13e | już w matrycy tylko nie w MD |
| ISO 27001 / NIS2 | NIE | TAK §13e | już w matrycy tylko nie w MD |
| Prognozy cen frachtów/paliwa | CZĘŚĆ Macro geo (§2) | TAK §13e | już w matrycy tylko nie w MD |

### 2e. §13d (4)

B0 ma `plan_snapshot` i TT. V2 pogoda. V2b myto. V8 what-if.

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Zakazy jazdy (Nakordoni **Truck Bans**, nie kafelki) | NIE (B#16 = tiles) | TAK §13d | już w matrycy tylko nie w MD |
| NAPSPAN / DATEX II restrykcje (wymiary, osie, tunele) | NIE (V2b = myto) | TAK §13d | już w matrycy tylko nie w MD |
| Traffic zewnętrzny HERE / TomTom / PTV | NIE | TAK §13d | już w matrycy tylko nie w MD |
| Kontrfaktyczne przeplanowanie linii | CZĘŚĆ V8 | TAK §13d | już w matrycy tylko nie w MD |

### 2f. §13f — przetargi + metrologia (9)

Tender Radar (TED) jest w tabeli 3. To inny job niż SIWZ klienta.

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Analiza dokumentacji przetargowej (RFP/SIWZ) | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Playbook przetargowy | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Prospecting | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Auto-wypełnianie matrycy przetargowej | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Bid/no-bid | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Pomiar skuteczności przetargów | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Pomiar czasu jobu operatora | NIE | TAK §13f | już w matrycy tylko nie w MD |
| A/B testy UI | NIE | TAK §13f | już w matrycy tylko nie w MD |
| Testy zadaniowe z pilotami (SUS) | NIE | TAK §13f | już w matrycy tylko nie w MD |

### 2g. Matryca §2–§11 (poza falami już w tabeli 1) (22)

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Select & Drop | NIE | TAK §2 | już w matrycy tylko nie w MD |
| Pre-planning | NIE | TAK §2 | już w matrycy tylko nie w MD |
| Auto-assign resources | NIE | TAK §2 | już w matrycy tylko nie w MD |
| Mapa planistyczna 1000 + polygon | CZĘŚĆ T6 | TAK §2 | już w matrycy tylko nie w MD |
| Plan vs wykonanie (jakość planowania) | CZĘŚĆ P5 | TAK §2 | już w matrycy tylko nie w MD |
| Dystrybucja: podział FV kosztowej do sztuki | NIE | TAK §3 | już w matrycy tylko nie w MD |
| Charge templates | NIE | TAK §4 | już w matrycy tylko nie w MD |
| Market data giełd (Transporeon Insights, accepted price) | NIE | TAK §4 | już w matrycy tylko nie w MD |
| Intermodal bulk move | NIE | TAK §5 | już w matrycy tylko nie w MD |
| Giełda zleceń dla przewoźników partnerskich | NIE | TAK §6 | już w matrycy tylko nie w MD |
| Webhooki outbound | NIE | TAK §6 | już w matrycy tylko nie w MD |
| Bilety promowe w portalu | NIE | TAK §6 | już w matrycy tylko nie w MD |
| Rentowność wielowymiarowa | NIE | TAK §7 | już w matrycy tylko nie w MD |
| ADR advisor | NIE | TAK §8 | już w matrycy tylko nie w MD |
| Champion/challenger + drift detection | CZĘŚĆ V1 | TAK §9 | już w matrycy tylko nie w MD |
| AI summaries wątków mailowych | NIE | TAK §10 | już w matrycy tylko nie w MD |
| AI Rule Builder (chat → reguła jako dane) | NIE | TAK §10 | już w matrycy tylko nie w MD |
| AI chat agent (pytania o rekordy) | NIE (KB = SOP) | TAK §10 | już w matrycy tylko nie w MD |
| Carrier procurement agent | NIE | TAK §10 | już w matrycy tylko nie w MD |
| Saved views współdzielenie (zespół/org) | NIE | TAK §11 | już w matrycy tylko nie w MD |
| Słowniki per tenant | NIE | TAK §11 | już w matrycy tylko nie w MD |
| Numeracja per lokalizacja / oddział | NIE | TAK §11 | już w matrycy tylko nie w MD |

### 2h. §13a + MC §95 (5)

| Nazwa z PDF/MC | W stan-planu? | W matrycy/§13q/odrzuceniach? | Akcja |
|---|---|---|---|
| Segmentacja handlowa A/B/C | NIE | TAK §13a | już w matrycy tylko nie w MD |
| Wywiadownie (KRD / Coface / D&B / CreditSafe) | NIE | TAK §13a | już w matrycy tylko nie w MD |
| Data Normalization Engine (MC §95B) | CZĘŚĆ Unified Telemetry §13j | TAK inwentarz §95 → §12 | już w matrycy tylko nie w MD |
| AI Agent Runtime (MC §95J) | NIE | TAK inwentarz §95 | już w matrycy tylko nie w MD |
| Audit Engine (MC §95K) | CZĘŚĆ Lineage (§2) | TAK inwentarz §95 | już w matrycy tylko nie w MD |

**Suma wierszy §2a–2h: 24+35+18+19+4+9+22+5 = 136.**

---

## 3. Nigdzie — 0 silników

Ziarno 42 z audytu: **36** w §13q (tabele 2–3 MD) + **10** w rejestrze (tabela 4; rozszczepienia FOTA/Video/Driver). Nic z tej 42 nie wisi poza planem.

Alias z audytu B (nie dublować jako luka): AI Rule Builder = §10; Tacho Office = §13e; Axle Load Optimizer = Loading optimizer; Plan/Dynamic/Predictive ETA = V2; Document AI / Email Intelligence / Task Engine / Carrier Procurement = §10 / T5 / M-20; D&D Watchdog / Rollover = V3; Slot Intelligence / Secure Chain / Port Identity = §12; Cost Allocation / Make or Buy / TIME-TO-FIX / Driver Time Solver = §13j.

Nazwy z digestów (**Quote Engine**, **Rate Intelligence**, **Ocean Intelligence**, **Ferry OS**, **Warehouse OS**, **Digital Twin Fabric**, **Scientific Prediction Framework**, **Telematics Abstraction Layer**, **Omni Mobility Package Engine**, **Global Optimizer**, **DriverComplianceLedger**, **OMNI PORT CONNECT**, **Truck Slot Engine**, …) to synonimy wierszy z §2–§13j albo parasole. Nie inflacjować.

Świadomie poza ziarnem: 324 pola; konektory per marka (DFDS, Stena, …); SKU OmniTrack / OmniTacho / OmniFuel / OmniCold / OmniVision (własny HW/wideo = rejestr); GMV/ARR; plik MASTER BLUEPRINT (rejestr: nieistniejący).

---

## 4. MC 103 + katalog 120 — nie 1:1 z MD

[inwentarz-mc-pdf.md](inwentarz-mc-pdf.md) odhacza **nagłówki** §0–103 (MAT/ODR/ZAS) i **120 etykiet** powierzchni. Stan-planu ma 144 wiersze funkcji, nie 103+120. Przykłady rozjazdu: MC §75 „optymalizacja sieci” ≠ Network Design; katalog #7 Network planning ≠ §95E. Fałszywy pewnik „103 sekcje 1:1” został zdjęty w audycie — ten plik go nie przywraca.

---

## Źródła

- [stan-planu-funkcje.md](stan-planu-funkcje.md) — 47+25+37+35
- [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md) — ziarno 42
- [benchmark-tms-2026.md](benchmark-tms-2026.md) §12, §13j, §13q, rejestr
- [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md)
- digesty `chatgpt-pdf-digest-1.md` / `2` / `3`
- MC: nagłówki §0–103 i silniki §95 A–L — bez dumpa
