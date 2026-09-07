# Luki: rozmowa w oknie vs `stan-planu-funkcje.md`

**Data:** 2026-09-07. **Nie kanon.** Nie edytuje `stan-planu-funkcje.md`, `CURRENT.md`, PLAN. Zero commita.

**Transkrypt (grep `user_query`, bez dump całego JSONL):**  
`C:\Users\sebas\.cursor\projects\d-OMNIROUTE\agent-transcripts\2db73c11-b1f8-44d1-947a-79a8402254aa\2db73c11-b1f8-44d1-947a-79a8402254aa.jsonl`  
Komendy `user_query` operatora: MSG#2–#38 (linie 21–324). MSG#1 (linia 1) = wklejka Qargo + zrzuty SPEED + master-context. MSG#12/#24 = szum systemowy (pominięte).  
**Także:** [pola-wizja-2026-09.md](pola-wizja-2026-09.md), [benchmark-tms-2026.md](benchmark-tms-2026.md) §13g–p, karty [006](../_knowledge/market/006-telematics-hub.md)–[011](../_knowledge/market/011-poczta-ksiazka-nadawcza.md).

## Werdykt

`stan-planu-funkcje.md` w podsumowaniu pisze **0 BRAK** (18/5/0). To audyt **matrycy**, nie audyt **wierszy**.  
Kryterium tutaj: temat z rozmowy ma wiersz tylko gdy kolumna **Funkcja** w tabelach 1–4 go nazywa. Wzmianka w „Co robi” / „Minus” innego wiersza **nie** jest wierszem.

Skutek: wieczorne decyzje (flaga `paper_post`, drabina FV, USB, ML Kit, bbox, GBOX P0, zakazy jazdy, widok drobnica≠FTL, chatbot, bliźniak, przetargi, UX…) są w §13g–p / polach / kartach 006–011, ale w `stan-planu` **znikają w sklejkach** (`T6+X8`, `X9+X6`, `F9+F10`, `F11`, `V5+V6`, `C1+C7+C8`).

## Metoda

| Werdykt kolumny 2 | Znaczenie |
|---|---|
| **TAK** + cytat | Kolumna Funkcja nazywa temat — **nie** należy do BRAK (nie ma w tabeli poniżej). |
| **NIE** | Brak wiersza. |
| **NIE (wzmianka)** | Brak wiersza; temat schowany w komórce innego wiersza. |

Kolumna 3: [benchmark-tms-2026.md](benchmark-tms-2026.md) / [pola-wizja-2026-09.md](pola-wizja-2026-09.md) / karta 006–011 / [kolejka-propozycja.md](kolejka-propozycja.md).  
Kolumna 4: co dopisać **jako osobny wiersz** w `stan-planu` (gdy operator każe edytować tamten plik).

## Są wierszem (nie BRAK) — żeby nie dublować

| Temat | Wiersz `stan-planu` (cytat Funkcja) |
|---|---|
| Dedup NIP/VAT-EU | M10-1 dedup |
| Role kontrahenta / JDG | M10-2 role |
| Podzlecenie | T4 podzlecenia |
| Planning board Timeline/Blocks/Table/Legs | T6 board + X8 podkłady |
| Mapy: darmowe u usera + BYO u admina | T6 board + X8 podkłady |
| Książka nadawcza PP | F11 książka nadawcza |
| EPO (imię) | EN + EPO (F11) |
| ERP FS+FZ | F9 + F10 ERP + FV kosztowa |
| KSeF wystawia Omni | F1 KSeF live + C#22 |
| Tronik ATRAX4, Logisat | Native GPS poza P0 |
| Open-Meteo / pogoda pan-EU | V2 ETA + pogoda |
| Lejek oferty | X7 lejek oferty |
| SENT + katalog + blokada polisy | C1+C7+C8 |
| BDO/KPO/DIWASS | C6 odpady |
| Myto EU/EFTA | V2b myto EU/EFTA |
| Teltonika/Queclink | L1a Teltonika/Queclink |
| Giełdy GPS | V5b giełdy tracking |
| What-if (ogólny silnik) | V8 what-if |
| Karty pól poza Falą T | Karty pól fal D/P/X/F/C/V |
| Rewrite GraphQL/Django | C#1 |
| BIK / osoby prywatne | C#8 / C#7 |
| GAN na skanie | C#20 |
| Pola „324/32” jako tally | akapit Pola w podsumowaniu — **nie** wiersz funkcji (luka kompletności = wiersz Karty pól) |

---

## Tematy z rozmowy bez własnego wiersza

Źródła MSG = `user_query` w transkrypcie. Q = wklejka Qargo MSG#1.

| # | Temat z rozmowy | Jest w stan-planu? (TAK cytat / NIE) | Jest w matrycy/polach? | Co dopisać |
|---|---|---|---|---|
| 1 | Select & Drop (wiele zleceń → zasób) | **NIE.** T6 = „Timeline/Blocks/Table/Legs; darmowe on/off…” — bez Select & Drop. | TAK: matryca §2; kolejka T6 „select&drop” | Wiersz T6b Select & Drop + walidacje ładowność/ADR/okna/marża |
| 2 | Pre-planning (przestrzeń przed przypisaniem) | **NIE** | TAK: matryca §2; kolejka T6 | Wiersz T6c Pre-planning |
| 3 | Mapa: do 1000 zleceń + rectangle/polygon | **NIE** | TAK: matryca §2 | Wiersz T6d selekcja na mapie (lazy, nie initial 250 kB) |
| 4 | Markery: Collection trójkąt / Delivery kwadrat / Other koło + kolor statusu | **NIE** | CZĘŚĆ: §13k podkłady, zero markerów | Wiersz UI markerów planowania |
| 5 | Warstwy Satellite / Live Traffic / Truck Restrictions | **NIE (wzmianka).** Nakładki Parking/Fuel/… mają LEZ/ORM, nie truck restrictions ani satelitę. | CZĘŚĆ: §13k lista darmowych + nakładki | Wiersz nakładek: satelita, ruch live, restrykcje TIR |
| 6 | Saved views A+/A−, prywatne i zespołowe | **NIE** | TAK: matryca § UI `table_view` DONE | Wiersz „już w kodzie” + gęstość A+/A− na boardzie T6 |
| 7 | Email Intelligence (Outlook → Order) | **NIE** | TAK: matryca §1 RFQ z maila DONE M-32/M-28 | Wiersz 0/X: Email Intelligence (HITL, nie auto-zlecenie) |
| 8 | AI Summary | **NIE** | NIE jako silnik | Wiersz HZ: summary po HITL **albo** odrzut z powodem |
| 9 | AI Validation Rules (Qi) | **NIE** | CZĘŚĆ: T5 task engine „Nie LLM” | Wiersz: reguły = dane SQL; LLM nie pisze reguł |
| 10 | Chatbot klienta: raporty i pytania (MSG#6) | **NIE.** Knowledge Base = SOP; Operational Service Agent = ticket. | CZĘŚĆ: §13q KB; WhatsApp odroczone | Wiersz Customer Chat (HITL, RAG tylko SOP) **albo** odrzut/HZ |
| 11 | Consignment jako obiekt (Qargo) | **NIE** | CZĘŚĆ: D2 paczka; T1 stop | Wiersz T/D: consignment między order a stop |
| 12 | Stop Group | **NIE (wzmianka).** T1 minus: „`stop_group` rozstrzyga Plan” | TAK: matryca §2 stop_group | Wiersz T1b stop_group |
| 13 | Auto-assign zasobów | **NIE.** T7 w stan-planu = kurs VAT, nie assign. | TAK: matryca §2 T7 auto-assign — **kolizja ID z T7 FX** | Wiersz T6e auto-assign; rozdzielić ID od T7 kursu |
| 14 | Subcontractor bidding | **NIE** | CZĘŚĆ: M-30/M-31 w kodzie, nie w tabelach stan-planu | Wiersz 0/P: bidding + spread na `charge` |
| 15 | Widok dyspozytora drobnicy ≠ spedytor FTL A→B (MSG#6) | **NIE** | TAK: matryca wiersz widoki per rola T6/D | Wiersz T6/D: trzy boardy, jeden model stop/trip |
| 16 | Cyfrowy bliźniak „na wszystko”, od dnia 1 (MSG#6–7) | **NIE.** B0 = ledger zdarzeń, nie 8 twinów. Odroczone „digital twins pełne” poza tabelą 4. | CZĘŚĆ: B0/V1; PDF 8 twinów | Wiersz: twin = B0+V1 od startu; pełne twiny = HZ z listą |
| 17 | Twin auto-planning: what-if linie drobnicowe NO/DE/SE + traffic + warunki drogi (MSG#8) | **NIE (wzmianka).** V8 = „Silnik scenariuszy na danych B0” bez linii NO/DE/SE. | CZĘŚĆ: V8; Linehaul §13j | Wiersz V8b: scenariusz linii + TT z actuals + zakazy + pogoda |
| 18 | Zakazy jazdy (święta/wakacje/upały, etransport.pl, darmowe API) (MSG#8) | **NIE.** „Nakordoni / Carto / Esri tiles” = **licencja kafelków**, nie Truck Bans. | TAK: matryca zakazy jazdy (Nakordoni Truck Bans + Nager.Date + `driving_ban_rule`) | Wiersz V: katalog `driving_ban_rule` + feed; etransport = kuracja nie API |
| 19 | Ograniczenia drogi: wymiary, masa, nacisk na oś (MSG#8) | **NIE.** V2b osie = taryfa myta na pojeździe, nie zakaz odcinka. | CZĘŚĆ: overlay LEZ; nie ORM mass/axle | Wiersz V: restrykcje odcinka (dane + źródło) |
| 20 | Traffic live + historyczny do TT (MSG#8) | **NIE (wzmianka).** V2 „historical/live” = warstwy ETA, nie feed korków. | CZĘŚĆ: §13k overlay_traffic; cache tras §13j | Wiersz V2c: źródło ruchu + TTL; nie LLM |
| 21 | Moduł przetargowy: SIWZ, playbook, kontakty z internetu, auto-wypełnienie matrycy, fit tras do sieci, pomiar rentowności (MSG#10) | **NIE.** Tender Radar = TED; P6 = ważność oferty. | CZĘŚĆ: Tender Radar TO_VERIFY; P6 | Wiersz HZ: Tender Playbook (HITL); zakaz scrapingu kontaktów; matryca = SQL+HITL nie „bez błędów LLM” |
| 22 | Pomiar naukowy UX/UI (MSG#10) | **NIE** | NIE | Wiersz ops: telemetria UI (PostHog już w stosie) + protokół A/B; nie scoring osoby |
| 23 | Wywiadownie KRD / Coface / D&B / CreditSafe — analiza JDG HITL (MSG#7) | **NIE (wzmianka).** C#8 „Zostają KRD…” w wierszu **odrzutu BIK**, nie jako funkcja. | CZĘŚĆ: karta 005 | Wiersz F/C: lookup wywiadowni + HITL; nie auto-score JDG |
| 24 | Adaptery P0 nazwane: GBOX, IKOL, Flotis, Wialon (MSG#11) | **NIE (wzmianka).** V5 Co robi: „P0 PL (GBOX, IKOL, Flotis, Wialon)”. Native GPS poza P0 = reszta. | TAK: §13g; karta 006 | Wiersz V5-P0: cztery adaptery + status docs (GBOX za loginem) |
| 25 | Unified Telemetry: paliwo, CAN, DTC, temp, heading (MSG#11 + PDF) | **NIE** | TAK: pola `position_event` §3.2; §13j UTM | Wiersz V5: kontrakt pól PositionEvent (nie `tracking_event`) |
| 26 | Diagnostyka spedytora: za drogo vs brak aut vs kompetencja (MSG#11) | **NIE (wzmianka).** V5b = tracking + `exchange_message`. | TAK: §13g diagnostyka; kolejka V5b metryki jobu | Wiersz V/X: metryki jobu (`entity_event`) bez podsłuchu |
| 27 | `quoted_amount` na `carrier_inquiry` | **NIE** | TAK: pola §3.6; kolejka V5b | Wiersz M-30 rozszerzenie: cytowana cena z naszego kanału |
| 28 | IMGW / DWD / Météo-France suplement Open-Meteo | **NIE (wzmianka).** V2 wymienia Open-Meteo, nie narodowe feedy. | TAK: §13h; karta 007 | Wiersz V2-suplement: IMGW/DWD/Météo-France |
| 29 | Instrukcja admina: skąd wziąć API map (MSG#20) | **NIE** | TAK: plik `podklady-map-admin.md` (poza tabelami stan-planu) | Wiersz X8b: instrukcja w UI + plik; nie nowy kod per vendor |
| 30 | Nazwany katalog darmowych P0: OpenFreeMap, GUGiK, CyclOSM, HOT, Carto… | **NIE.** T6+X8 bez nazw. | TAK: §13k; pola `map_basemap` §5.1 | Wiersz X8: seed katalogu + `is_blocked` osm.org |
| 31 | Drabina match FV kosztowej (6 szczebli SQL, progi 1-klik) (MSG#23) | **NIE (wzmianka).** F9+F10: „ranking SQL → HITL”, słowo **drabina** nie pada. | TAK: §13m; pola `invoice_match_candidate` §7.5; karta nie 006–011 | Wiersz F10b: drabina `shipment_ref` → identifiers → NIP+kwota+data → wątek → lane → unassigned |
| 32 | `shipment_ref` twardy numer (wydruk, QR, mail, FV podwykonawcy) | **NIE (wzmianka).** D9: „QR `shipment_ref`”. | TAK: pola `shipment.shipment_ref` §2.1; §13m/n | Wiersz: `shipment_ref` (F10+D9) — obowiązkowy na wychodzących |
| 33 | FV z innych kontynentów (brak NIP) → lista + mail „podaj numer Omni” | **NIE** | TAK: §13m | Wiersz F10c: brak zgadywania; `mail_draft` HITL |
| 34 | Jedna FZ → wiele zleceń; suma linii = kwota (SQL) | **NIE** | TAK: pola `purchase_invoice_allocation` §10.2 | Wiersz F10d: alokacja; model nie sumuje |
| 35 | Split HITL lewo dokument / prawo wartość+rodzaj+pewność+edycja (MSG#27) | **NIE (wzmianka).** X9+X6: „bbox + split HITL”. | TAK: §13o; karta 010; pola §7.3 | Wiersz X9b: kontrakt UI split (już makieta ui-04; brak pewności per pole w kodzie) |
| 36 | bbox + `confidence` + `operator_override` | **NIE (wzmianka).** X9 wymienia bbox. | TAK: pola §7.3 | Wiersz X9c: pola kandydata (JSONB), nie nowa tabela |
| 37 | ML Kit (Android, `BASE_WITH_FILTER` / `FULL` nie na FV) + VisionKit (iOS) (MSG#27/29) | **NIE (wzmianka).** Scanbot / cloud DI: „OpenCV+ML Kit/VisionKit = P0 bez tej licencji”. | TAK: §13o; karta 010; pola `capture_engine` / `mlkit_mode` §7.4 | Wiersz X9-capture: ML Kit/VisionKit P0; Scanbot zostaje TO_VERIFY |
| 38 | Enhance „skaner płaski”: warp, deskew, biel, kolor vs B/W, Lanczos ~300 (MSG#29) | **NIE (wzmianka).** X9: „OpenCV (~300 DPI Lanczos)”. | TAK: §13o; karta 010; `scan_enhance_run` §7.4 | Wiersz X9-enhance: kroki OpenCV; oryginał zostaje; zakaz GAN już C#20 |
| 39 | Quality gate / „zrób zdjęcie ponownie” (Laplace, prostokąt) | **NIE (wzmianka).** X9: „Gate + …” | TAK: §13o; Photo POD w matrycy | Wiersz X6/X9: gate przed extractem |
| 40 | Flaga `paper_post` = FV papierowa → PP (MSG#31) | **NIE (wzmianka).** F11: „`paper_post` → `postal_dispatch`”. | TAK: pola §9.1–9.2; karta 011 | Wiersz F11a: `delivery_channel` na `party` i `sales_invoice`; papier ≠ wyłączenie KSeF |
| 41 | Wejście `numer_nadania`: USB/HID, zwrotka EN, wklejenie+checksum (MSG#30) | **NIE.** F11 i EN+EPO milczą o USB/HID. | TAK: §13p kolejność 1–3; karta 011 „USB/HID” | Wiersz F11b: trzy ścieżki numeru; skaner HID = klawiatura |
| 42 | AI tylko tam, gdzie ROI + dowód naukowy (MSG#33) | **NIE.** Jest akapit AI w podsumowaniu, **nie** wiersz funkcji. | TAK: `ai-nauka-i-dowody.md`, `ai-gdzie-uzasadnione.md`, §10 | Wiersz ops: brama „AI w module” (HITL extract tak; kalkulator/GAN/scoring nie) |
| 43 | Adaptery ERP osobno: Optima, XL, nexo, GT + agent outbound (MSG#21–22) | **NIE (wzmianka).** F9+F10 zbiorczo; ERP P0 = **licencje**. | TAK: §13l; pola `erp_connector` §6; `erp-fk-adapter.md` | Wiersz F9b: katalog systemów P0 (pięć adapterów, nie jeden) |
| 44 | Parser FA(3) deterministyczny (KSeF zakup, nie LLM) | **NIE (wzmianka).** F9+F10: „XML FA(3) bez LLM”. | TAK: §13m | Wiersz F10e: XSD parser vs extract skanu |
| 45 | Cost Allocation Engine (DIRECT/SHARED/…) | **NIE** | TAK: §13j | Wiersz F/V: klucze alokacji jako dane; marża zostaje w `charge` |
| 46 | TIME-TO-FIX (SAFE/AMBER/RED + przyczyna) | **NIE** | TAK: §13j | Wiersz V2/V6 |
| 47 | Dwa ETA: fizyczne vs prawne/operacyjne | **NIE** | TAK: §13j | Wiersz V2+V7 |
| 48 | Ferry rest (art. 9) + ferry watchdog (ETA vs cut-off) | **NIE.** V7 = tacho/posting ogólnie; V3 = D&D morze. | TAK: §13j | Wiersz T1/V7: `FERRY_REST_EVENT`; V3b prom |
| 49 | Driver Time Solver (warianty A–I) | **NIE** | TAK: §13j | Wiersz V7b: warianty jako dane; apka nie „poprawia” tacho |
| 50 | Legal Feasibility Check + symulacja minuta-po-minucie | **NIE** | TAK: §13j | Wiersz C/V: wynik = ryzyko, nie wyrok LLM |
| 51 | Geofence → waiting charge (HITL, nie auto-`charge`) | **NIE** | TAK: §13j | Wiersz V5+P |
| 52 | Elektroniczna karta drogowa | **NIE** | TAK: §13j | Wiersz V7/F |
| 53 | Fuel fraud / anomalia paliwa (flaga recenzji, nie wyrok) | **NIE.** Fuel Price Intelligence = ceny stacji. | TAK: §13j | Wiersz V/HZ: expected vs actual + GPS; nie scoring osoby |
| 54 | Profil wysokości trasy (osobno od pogody) | **NIE** | TAK: §13j | Wiersz V |
| 55 | VAT Engine (traktowanie+stawka+podstawa, B2B, nie LLM) | **NIE** | TAK: §13j | Wiersz F/C: katalog reguł SQL |
| 56 | Terms AI na obcym zleceniu (ryzyko + HITL) | **NIE** | TAK: §13j | Wiersz X |
| 57 | Słownik naczep (Curtainsider, Mega, Reefer…) + osie | **NIE.** T2 minus: osie w katalogu pól, nie karcie T2. | TAK: §13j; pola `axle_count` na `resource` | Wiersz T2b: kind naczepy + osie (myto czyta to samo) |
| 58 | Cache tras (TTL traffic/trasa/LEZ) | **NIE** | TAK: §13j | Wiersz V routing |
| 59 | Akceptacja oferty z języka maila („akceptujemy 1850 EUR”) → szkic HITL | **NIE** | TAK: §13j; M-29 CZĘŚĆ | Wiersz X: extract → szkic shipment; HC-04 |
| 60 | Groupage CMR (osobny CMR na grupę dostaw) | **NIE (wzmianka).** D9: „CMR/SSCC/ZPL”. | TAK: §13n wzorzec Qargo | Wiersz D9b: CMR groupage per stop group |
| 61 | Make or Buy (własny tabor vs giełda vs sieć) | **NIE (wzmianka).** OMNI Market Orchestrator = parasol. | TAK: §13j | Wiersz V: ten sam ładunek, koszt+ETA+FIX; HITL |
| 62 | Bliźniak urzędu (proces/deadline, nie udawanie urzędu) | **NIE** | TAK: §13j | Wiersz C/HZ |
| 63 | Dock time window (dok, palety, naczepa, ADR, waga) | **NIE** | TAK: §13j; D3 CZĘŚĆ | Wiersz D3b |
| 64 | Opportunity Engine (oszczędność/ROI/owner) | **NIE** | TAK: §13j | Wiersz V/HZ |
| 65 | Dwie perspektywy UI: Operator OS vs Enterprise (jeden core) | **NIE (wzmianka).** C#25 odrzuca „dwa produkty”; nie opisuje dwóch perspektyw. | TAK: §13j; X1 vs T6 | Wiersz X1/V6: ten sam model, inny portal |
| 66 | FSC per usługa (nie jeden globalny %) | **NIE (wzmianka).** P1–P4: „FSC”. | TAK: §13j; P3 | Wiersz P3b: FSC jako dane per usługa |
| 67 | Integration Hub (telematics / porty / prom / cło / ERP / WMS) jako warstwa | **NIE** | CZĘŚĆ: sklejki V5, HZ konektory, F9, D1 „nie WMS” | Wiersz ops: hub = katalog konektorów, nie nowy silos |
| 68 | Air (lotnicze) jako moda | **NIE.** `shipment_leg` dziś road/rail/china_rail/ocean_lcl. | NIE w §13g–p | Wiersz HZ: air **albo** świadomy POMIŃ |
| 69 | WMS pełny | **NIE (wzmianka).** D1–D3 minus: „Nie pełny WMS”. | TAK jako granica D | Wiersz odrzut/HZ: WMS poza zakresem drobnicy D1–D3 |
| 70 | Copilot / Email AI / Document AI jako warstwa (Q §21) | **NIE.** X9 = skan; Ocean Email AI = §13q. Brak warstwy. | CZĘŚĆ: §10 AI; Ocean Email AI sekcja 2 | Wiersz: AI CORE = extract HITL + agenci §13q; nie chatbot-kalkulator |
| 71 | Factoring / CFO jako joby z wklejki Qargo | **NIE (wzmianka).** F5/F7 = TO_VERIFY zbiorczo; wieża V6 = stock→EBITDA. | CZĘŚĆ: kolejka F5/F7 | Rozdzielić wiersze F5 diety i F7 faktoring (dziś sklejone w sekcji 3) |
| 72 | `stop_group` + intermodal resources na boardzie (Q §7) | **NIE** | CZĘŚĆ: T2 resource; T6 | Wiersz T6f: zasób intermodal na boardzie |
| 73 | QR sieci: `tenant+shipment+package+document_kind` + skan od razu vs HITL bez kodu (MSG#26) | **NIE (wzmianka).** D9: „QR `shipment_ref`”; „Bez kodu Omni = HITL”. | TAK: §13n; karta 009; pola §8.3–8.4 | Wiersz D9c: dwa tory skanu (nasz QR vs obcy) |
| 74 | Koszt znaczka PP = `charge` + `source_ref` (nie pole na książce) | **NIE** | TAK: §13p; pola §9 | Wiersz F11c: znaczek na `charge` (wymaga leftover P0 `source_ref`) |
| 75 | Pola HITL: `hitl_confidence_*`, `invoice_match_suggest_min`, `telematics_grace_days` (MSG#32 „dodaj pola”) | **NIE** | TAK: pola §1.2 | Wiersz M-03: klucze allowlisty (nie sekrety) |

---

## Liczba BRAK

**BRAK = 75** (wiersze 1–75 w tabeli).  
To nie jest „cisza w matrycy”. To **cisza w kolumnie Funkcja** pliku, z którego operator ma podjąć decyzję.

Poprzednie 0 BRAK zostaje prawdziwe tylko przy definicji z [audyt-rozmowa-vs-plan.md](audyt-rozmowa-vs-plan.md) (decyzja jest gdzieś w §13/kolejce). Przy definicji operatora MSG#38 (pola, wizualizacje, integracje, AI, **każdy** pomysł jako pozycja planu) — **75 braków wierszy**.

## 20 nazw (pierwsze z listy BRAK)

1. Select & Drop  
2. Pre-planning  
3. Mapa 1000 + polygon  
4. Markery stopów  
5. Satellite / Traffic / Truck Restrictions  
6. Saved views A+/A−  
7. Email Intelligence  
8. AI Summary  
9. AI Validation Rules  
10. Chatbot klienta  
11. Consignment  
12. Stop Group  
13. Auto-assign  
14. Subcontractor bidding  
15. Widok drobnica ≠ FTL  
16. Cyfrowy bliźniak na wszystko  
17. Twin what-if linie NO/DE/SE  
18. Zakazy jazdy / etransport  
19. Ograniczenia masa/oś/wymiary  
20. Traffic do TT  

## Co z kart 006–011 i pól

Karty market **mają** GBOX P0, Open-Meteo, drabina, USB/HID, `paper_post`, ML Kit, split, QR. Katalog pól **ma** 324 wiersze. `stan-planu` **nie przeniósł** tych nazw do kolumny Funkcja — stąd BRAK tutaj przy TAK tam.

## Świadome nie-BRAK (żeby nie puchnąć tabeli)

Nie liczone: follow-upy systemowe; `/noc`; canvas vs MD; „unia SPEED+Qargo” jako slogan; stack Qargo (GraphQL/Django) — jest C#1.
