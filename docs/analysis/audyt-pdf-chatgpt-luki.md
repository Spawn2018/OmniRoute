# Audyt PDF ChatGPT — nazwane funkcje/silniki poza matrycą i rejestrem

**Data:** 2026-09-07 · **Nie kanon.** Nie wpięte w PLAN/CURRENT.

**Werdykt:** operator ma rację. Poprzednie „103 sekcje 1:1” i [inwentarz-mc-pdf.md](inwentarz-mc-pdf.md) odhaczały **nagłówki MC** oraz **wybrane** nazwy z digestów. Nie były inwentarzem każdej **nazwanej funkcji/silnika** z PDF (376 s.).

**Luki (ani wiersz w matrycy, ani rejestr odrzuceń):** **42**.

Źródła: digesty `chatgpt-pdf-digest-1/2/3.md` · MC §0–103 / katalog §92 / silniki §95 · [benchmark-tms-2026.md](benchmark-tms-2026.md) (§1–13p + rejestr) · [kolejka-propozycja.md](kolejka-propozycja.md). Pola (CMR, dock, Local Charge…) **nie** są lukami — idą przy `/plan-modul` (ADR-0004).

## Metoda

Ziarno = **nazwa** silnika/funkcji z PDF lub MC. „Jest w matrycy”, gdy ta nazwa (albo jednoznaczny synonim w tym samym wierszu) występuje w tabeli funkcji albo w rejestrze odrzuceń. Kawałki rozrzucone po falach **nie** zaliczają nazwy. Świadomie nie liczę: GMV/wyceny spółki (rejestr), stack Django (ADR-0004), 400 kolumn, konektorów per marka (DFDS, Stena…) — te ostatnie to katalog przy umowie, nie osobny silnik.

Fałszywe pewniki z inwentarza: MC §75 „optymalizacja sieci” → rzekomo §13e, a w §13e **nie ma** takiego wiersza (jest VRP/bin packing i network costing). MC §92 #7 Network planning ≠ Network Design.

## A. Luki

| ID | Funkcja z PDF/MC (strona/§) | Czy w matrycy? | Czy odrzucone? | Propozycja |
|---|---|---|---|---|
| L-01 | **AI Margin Guard** — trip stratny; FSC poniżej rynku; oferta przewoźnika powyżej mediany; sugerowana cena sprzedaży (PDF s.23–24) | NIE (jest Expected vs Actual P5 i Digital CFO, nie ten strażnik) | NIE | **Dodać** do matrycy (P/V, HITL, SQL nie LLM) |
| L-02 | **Device Management / FOTA** — IMEI, provisioning, firmware, heartbeat, SIM, OTA (PDF s.86; Teltonika FOTA WEB s.83–86) | NIE | NIE (odrzucony jest **własny** HW/firmware, nie zarządzanie cudzym urządzeniem) | **Dodać** (V5, pakiet Teltonika/Queclink + BYO) |
| L-03 | **Tender Radar** — TED Search API + eForms, nowe przetargi publiczne (PDF s.169) | NIE (13f = SIWZ klienta / prospecting firm, nie feed TED) | NIE | **Dodać** HZ; **TO_VERIFY** dostęp/licencja TED |
| L-04 | **Operational Service Agent** — ticket: klasyfikacja → root cause → propozycja (np. przesuń slot) → HITL (PDF s.140–141) | NIE (jest Customer Chat i IT Support Agent — inny job) | NIE | **Dodać** (X/HZ) |
| L-05 | **Blank sailing prediction** — predykcja odwołanego rejsu (PDF digest 3, warstwa Ocean OS / sea predictions) | NIE (V3 = D&D + rollover ETD/ETA, nie blank sailing) | NIE | **Dodać** (V3) |
| L-06 | **IMO DCS / CII** — zużycie paliwa statków ≥5000 GT, dane do CII (PDF s.159–160, 348) | NIE (C5 = GLEC/GHG, nie IMO) | NIE | **Dodać** (C5/HZ); **TO_VERIFY** kto składa (armator vs spedytor) |
| L-07 | **EU ETS + FuelEU Maritime** jako compliance (PDF s.159–160) | NIE (ETS pojawia się jako składnik ceny promu, nie silnik) | NIE | **Dodać** (C/HZ); **TO_VERIFY** obowiązek tenanta |
| L-08 | **Dispatch Agent** — agent AI listy s.354 (obok Transport/Legal/CFO Advisor) | NIE (13e = Transport / ADR / Customs / Legal Advisor) | NIE | **Dodać** jako alias T6+V7 albo wiersz HZ (HITL) |
| L-09 | **Cabotage Engine + RTPD** — licznik kabotażu; powrót kierowcy i pojazdu (PDF s.108–109, 328; dyrektywa 2020/1057) | NIE (V7 = tacho/prom art. 9; F5 = płace/delegowanie, nie kabotaż/RTPD) | NIE | **Dodać** (C/V7); **TO_VERIFY** prawo per kraj |
| L-10 | **Combined Transport** — operacja jako typ Mobility Package + dyrektywa transport kombinowany (PDF s.108, 328) | NIE (intermodal = nogi/Huckepack, nie reżim prawny combined) | NIE | **Dodać** (C); **TO_VERIFY** |
| L-11 | **ZSL / SENT-GEO / e-TOLL gateway (Level 2)** — Omni jako brama GPS → PUESC / e-TOLL (PDF s.257–259) | NIE (C1 = zgłoszenie SENT; 13h = taryfa e-TOLL jako myto, nie certyfikat ZSL) | NIE | **Dodać** HZ; **TO_VERIFY** kto może być ZSL |
| L-12 | **Biała lista jako bramka płatności** — NIP+rachunek przed przelewem, weryfikacja masowa (PDF s.256–257, 344) | NIE (C3 = lookup; F4 = CAMT; nie brama „nie płać”) | NIE | **Dodać** (F4/C3) |
| L-13 | **Sankcje: UBO + bank + HS/CN + port** (PDF s.183–184) | CZĘŚĆ nazwy brak: M-53 ULEPSZ „statki/ładunki/trasy”; **UBO i bank nie są nazwane** | NIE | **Dodać** zakres do wiersza M-53 (nie nowy silos) |
| L-14 | **Knowledge Base** — trzecia warstwa chatu: Agent / Support / KB (PDF s.9–10) | NIE | NIE (RAG na wycenie jest odrzucony; RAG na SOP/dokumentacji — HC-08 — wolno) | **Dodać** (X/HZ), zakres = SOP/docs, nie stawki |
| L-15 | Nakładki map: **Parking, Fuel, Border, Ferries, Customs, Weather** (PDF s.20) | NIE (13k: ruch, LEZ, OpenRailwayMap) | NIE | **Dodać** do katalogu nakładek §13k (dane, on/off) |
| L-16 | **Fuel Price Intelligence / rekomendacja stacji** — teraz vs następna stacja, €, km (PDF s.204–206) | NIE (13j = anomalia paliwa; 13c = karty/zbiorniki; B0 = indeks; nie POI stacji) | NIE | **Dodać** (V/HZ); **TO_VERIFY** źródło cen stacji |
| L-17 | **Topologie sieci drobnicowej** — hub&spoke, milk-run, wiele magazynów, wiele krajów jednocześnie (PDF s.130, 134–135; MC §23) | NIE (D1 = linie+cutoff, „nie optymalizator”; inwentarz fałszywie dał MAT) | NIE | **Dodać** (D1 Plan / V network design) |
| L-18 | **Container Readiness Engine** (PDF s.285) | NIE (Slot Intelligence = który slot; T3 = obiekt kontenera) | NIE | **Dodać** (HZ Port OS, po konektorze) |
| L-19 | **Port Congestion Prediction** (PDF s.285, 292) | NIE | NIE | **Dodać** (V/HZ); V1 ledger |
| L-20 | **Port Marketplace** — katalog Port→Terminal→Depot→Empty→Customs + capabilities/fees (PDF s.293) | NIE (jest Port Identity = sejf poświadczeń) | NIE | **Dodać** (HZ, dane) |
| L-21 | **Terminal Appointment & Gate OS** + **dynamic reschedule** 8–9 kroków (PDF s.291–292, 309–310); 14 kroków awizacji (s.298) | NIE (matryca ma **SDK konektora** 14 funkcji ≠ orchestration bramy) | NIE | **Dodać** (HZ); nie obiecać „zawsze zarezerwujemy” (L-37) |
| L-22 | **Data licensing layer** — per dataset: source, license, geography, frequency, usage restrictions (PDF s.368) | NIE (`source_ref` ≠ licencja/geografia/ToS) | NIE | **Dodać** (ops/C, tabela licencji źródeł) |
| L-23 | **Omni Graph** — zdarzenie `ContainerETAChanged` → slot, truck ETA, magazyn, D&D, revenue risk (PDF s.366–367) | NIE (Business Impact Graph = korporacja SKU→EBITDA; Memory Graph = „co zadziałało”) | NIE | **Dodać** (V; szyna na `entity_event` z B0) |
| L-24 | **Network Design Optimizer** — lokalizacja hubów / struktura linii (MC §95E „network design”; MC §75) | NIE (Multi-Objective = wagi na istniejącą sieć; VRP = przydział; costing ≠ design) | NIE | **Dodać** HZ (OR, nie LLM) |
| L-25 | **Demand Engine** — popyt na lane; track record „Demand 87,4%” (PDF s.172–176) | NIE (V1 = ledger ogólny; F Prediction Engine w MC §95 wymienia demand, matryca nie) | NIE | **Dodać** (V1 rodzaj predykcji) |
| L-26 | **OMNI Market & Network Orchestrator** — giełdy+sieci+własna flota+magazyn+finansowanie jako źródła zdolności; *nie* moduł „giełda” (PDF s.130) | NIE jako nazwa (są Make or Buy, D8, 13g) | NIE | **Dodać** jako nazwany parasol V (albo alias Make or Buy+D8 w jednym wierszu) |
| L-27 | **Macro & Geopolitical Intelligence** — warstwa sygnałów (energia, polityka, żegluga) (PDF s.165–172) | NIE (13e = *wynik* „prognoza cen z czynnikami geo”, nie silnik sygnałów) | NIE | **Dodać** (V/HZ Market Intelligence); korelacja ≠ przyczynowość zostaje |
| L-28 | **Ocean Email AI** — Customer RFQ → carrier RFQ → mail → parse → quote → HITL; pomiar response (PDF s.332–333) | NIE jako nazwa (Email Twin + P4 + M-20 to inne powierzchnie) | NIE | **Dodać** (X/P ocean, HITL) |
| L-29 | **Logistics Autopilot** — dojrzałość 0–8 (pokazuje→…→wykonuje w granicach) (PDF s.252, 358) | NIE | NIE | **Dodać** jako regułę `/plan-modul` / DoD automatyzacji (nie osobny produkt) |
| L-30 | **Lineage** — data lineage + model lineage + decision lineage (PDF s.367–368) | NIE (Decision Ledger i model card to wycinki) | NIE | **Dodać** (V1/ops) |
| L-31 | **FerryGateway** — otwarty standard one-to-many (lista operatorów PDF s.67–68) | NIE (HZ „promy API” bez nazwy standardu) | NIE | **Dodać** jako P0 protokół promów; **TO_VERIFY** dostęp |
| L-32 | **Driver Score / Driver Profitability** — Safety/Fuel/Smoothness/… + revenue/fuel/accident cost (PDF s.50) | NIE | NIE | **Odrzucić** — scoring osoby/pracownika (AI Act + art. 22 RODO); KPI pojazdu/tripa zostają w SQL |
| L-33 | **Video AI / DMS / ADAS / OmniVision** — telefon, zmęczenie, kamery, „video available” na incydencie (PDF s.46–47, 53–55) | NIE | NIE (odrzucony własny GPS, nie wideo) | **Odrzucić** własny produkt kamer; BYO Webfleet video = **TO_VERIFY** prawo pracy / AI Act |
| L-34 | **VAT OSS / IOSS** (PDF s.344) | NIE | NIE | **Odrzucić** — B2C już poza produktem; B2B OSS nie jest jobem tenanta |
| L-35 | **Benchmarki między tenantami z danych poufnych** bez zgody/umowy (MC §93 zasada 5) | NIE jako zakaz w rejestrze (HC-01 = SQL, nie produkt Market Intelligence) | NIE | **Odrzucić** w rejestrze; Market Intelligence tylko dane licencjonowane / własne |
| L-36 | **Selenium / obejście zabezpieczeń terminala** (PDF s.309, 296: zakaz; portal-only = controlled manual) | NIE w rejestrze (13e ma „portal-fallback” — za szerokie) | NIE | **Odrzucić** automatyzację logowania do portalu terminala; fallback = zadanie człowiekowi |
| L-37 | Gwarancja **„zawsze zarezerwujemy slot”** (PDF s.290: capability matrix, CargoCard, brak API) | NIE | NIE | **Odrzucić jako gwarancję**; capability per terminal = dane (L-20/L-21) |
| L-38 | **TachoSync / zdalny odczyt DDD** jako konektor (PDF s.83–86, 328; „tylko gdzie urządzenie umie”) | NIE jako nazwa (V7 = tacho ogólnie) | NIE | **TO_VERIFY** per model; dodać do V7 po potwierdzeniu |
| L-39 | **Border Crossing Intelligence** — warstwa ETA „BORDER” + nakładka (PDF s.20, 1588 digest-1) | NIE | NIE | **TO_VERIFY** źródło czasów odprawy; dodać do V2+L-15 albo odrzucić brak API |
| L-40 | **JPK jako moduł Omni** (PDF s.256–257, 344 lista fiskalna) | NIE jako osobny wiersz (13l: JPK zostaje w FK) | NIE w rejestrze | **Odrzucić** — prawda JPK w ERP; adapter nie liczy |
| L-41 | **Early Warning** poziomy GREEN/AMBER/RED/**BLACK** (PDF s.212–213, 350–351) | NIE jako nazwa (V6 = łańcuch skutków, bez BLACK / nazwy Early Warning) | NIE | **Dodać** do V6 (słownik statusów wieży) |
| L-42 | **e-Doręczenia** (inna niż książka PP) — wspomniane w prozie 13p „HZ”, **brak wiersza funkcji i braku w rejestrze** | NIE w tabeli funkcji | NIE | **Dodać** HZ albo **odrzucić** „nie w v1”; dziś tylko zdanie w 13p |

## B. Nie luka — ta sama funkcja pod inną nazwą

Żeby nie inflacjować: **AI Rule Builder** = §10 „Chat-based validation rules”; **Tacho Office** = 13e „Wirtualne biuro rozliczeń czasu pracy”; **Axle Load Optimizer** = 13e Loading optimizer (naciski osi); **Plan/Dynamic/Predictive ETA** = §9 planned/historical/live/risk-adjusted + 13j dwa ETA (fizyczne/prawne); **Document AI / Email Intelligence / Task Engine / Carrier Procurement** = §10 / T5 / M-20; **D&D Watchdog / Rollover** = §5 + V3; **Slot Intelligence / Secure Chain / Port Identity** = §12; **Cost Allocation / Make or Buy / TIME-TO-FIX / Driver Time Solver** = 13j.

Katalog MC §92 (120 etykiet powierzchni) nadal jest zmapowany *grubo* — problemem nie jest CRM/FTL/KSeF, tylko **silniki nazwane w PDF, które ginęły w nagłówku**.

## C. Co z kolejki / HZ nadal nie zamyka luki

Kolejka V3 = „D&D watchdog + rollover” — **bez** blank sailing, congestion, readiness, Gate OS. HZ „promy API” **bez** FerryGateway. HZ „terminal connectors” = SDK, **bez** Appointment & Gate OS. To potwierdza L-05, L-18–L-21, L-31.

## D. Liczba

| | n |
|---|---|
| Unikalne luki (sekcja A) | **42** |
| Dodać do matrycy (główna propozycja) | 32 (L-01–L-31, L-41) |
| w tym dodać **i** TO_VERIFY API/prawo | 9 (L-03, L-06, L-07, L-09, L-10, L-11, L-16, L-31 + zakres L-21) |
| Odrzucić z powodem | 7 (L-32–L-37, L-40) |
| Głównie TO_VERIFY | 2 (L-38 TachoSync, L-39 Border) |
| Dodać albo odrzucić — decyzja operatora | 1 (L-42 e-Doręczenia) |

Nie commituję. Nie ruszam CURRENT/PLAN. Wpięcie = decyzja operatora (wiersze w matrycy albo rejestr).
