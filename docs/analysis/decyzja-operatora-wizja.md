# Twarde fakty do decyzji operatora — wizja vs kanon

**To jest karta decyzji.** Kanon kolejki = [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) + [CURRENT.md](../state/CURRENT.md) (pin 2026-09-08).  
Źródła tej karty: [benchmark-tms-2026.md](benchmark-tms-2026.md) (matryca + rejestr odrzuceń + §13g–13p), [kolejka-propozycja.md](kolejka-propozycja.md), [ADR-0004](../adr/0004-benchmark-qargo-speed-2026.md) (przyjęta 2026-09-07).

**Rozdział, którego nie wolno zgubić**

| Warstwa | Co to jest | Co z `/noc` |
|---|---|---|
| **Kanon** | P0 + Fala O + Fala I + T/D/P/X/F/C/V w PLAN (pin 2026-09-08). Named parks parked. | Po `/noc <godzina>`: pomija parks, jedzie od P0. **Ta sesja nocy nie startuje.** |
| **Analiza** | Matryca, karty pól, ten plik | Zasila kanon; nie druga kolejka. |

**Kanon dziś (2026-09-08 / plaster 128.0):** Etap Plan. Następny = **P0** `charge.source_ref`, potem Fala O (O7/O8) i Fala I. Auth0 S53 / portale S55 / AIS **parked**. S21 parked. S50 park (job zasobu = T2). S54/S59 parked. M-02 konsument leftover. Nie zgaduj 71–212.

**Noc po pinie** (gdy operator poda godzinę) jedzie od P0, **nie** w named parks. Nie startować `/noc` w sesji pinu.

**ADR-0004 (2026-09-07, pin fal 2026-09-08):** stos zostaje. Benchmark zasila kolejkę — fale **wpięte**. HC bez zmian.

Pozostałe pozycje fal (D5–D7, F2–F8, V2–V4, V7–V8, HZ) są w [kolejka-propozycja.md](kolejka-propozycja.md); poniżej tylko **25** pozycji decyzyjnych na listę.

---

## A. W planie analizy (matryca / kolejka-propozycja)

Co daje operatorowi (job), plus mierzalny jeśli jest w źródle, ryzyko. Od 2026-09-08 pozycje A są w **kanonie PLAN** (P0/O/T/…); named parks nadal parked.

| # | ID | Job operatora | Plus (źródło) | Ryzyko / warunek |
|---|---|---|---|---|
| 1 | **M10-1** | Jeden kontrahent na NIP/VAT-EU/EORI/DUNS; duplikat = 409 z linkiem. Zapis bez identyfikatora biznesowego = odmowa. | Dedup w bazie, nie w głowie spedytora. Zakaz B2C egzekwowany technicznie (operator 2026-09-07). | Constraint bez M10-2 może skleić oddział z matką. |
| 2 | **M10-2** | Wiele ról na jednym `party` (klient i podwykonawca); JDG jako flaga; `parent_party_id` (grupa/oddział/inny płatnik). | Wzorzec Qargo „Company = customer i subcontractor” (API Concepts). | JDG → kredyt tylko HITL (AI Act / art. 22 RODO); nie auto-scoring. |
| 3 | **B0** | Log od dnia 1: `prediction_ledger`, `entity_event`, indeksy rynkowe obok `nbp_rate`, `plan_snapshot`, własne TT z actuals stopów. | Bez logu nie ma scorecardu predykcji ani „co by było gdyby” (wymaganie operatora + MC). | Silnik what-if = Fala V, nie B0. B0 bez T1 nie ma actuals TT. |
| 4 | **T1 `stop`** | Dyspozytor widzi punkt ZA/WY/cło/prom/terminal z oknem i statusem, nie samą nogę. | Luka vs Qargo Order/Stop (9/10 twierdzeń API potwierdzonych). Dziś `shipment_leg` = relacja, nie punkt. | Nie mapa. `stop_group` rozstrzyga Plan. |
| 5 | **T2 `trip`+`resource`** | Jednostka wykonawczo-kosztowa: pojazd/kierowca/naczepa + podwykonawca z `party`. To **job**, którego brakowało S50. | ADR-0004: pierwsza proponowana fala po named parks; park S50 (2026-09-04) = „brak jobu własne auto”, nie „nigdy zasób”. | Nie telematyka, nie czas pracy. Nie własny HW. |
| 6 | **T3 `container`** | Obiekt ISO 6346: plomby, PIN, terminale, D&D, VGM, reefer — karta pól w analizie. | SPEED/MC: kontener nie jest polem tekstowym na zleceniu. | Nie booking armatorski (HZ, API per carrier). |
| 7 | **T4 podzlecenia** | Zlecenie główne + relacje; rentowność = widok SQL na `charge`. | SPEED: wynik spływa na główne. | Zakaz drugiej tabeli marży (HC-03). |
| 8 | **T5 task engine** | Szablony zadań jako dane (warunki w SQL jak `applies_when`); checklista wyjazdu/dokumentów. | Qargo Task na Order/Trip. | Async dopiero z konsumentem outboxa (M-02 leftover). Nie LLM. |
| 9 | **T6 board + X8 podkłady** | Timeline/Blocks/Table/Legs; select&drop z walidacjami; mapa lazy; darmowe on/off u usera, płatne BYO u admina (HC-05). | Oś klientów Qargo: puste km 31% UK / 25,9% UE (59 newsów + 44 case’y). | Mapa poza initial 250 kB. Nie AIS. Zakaz `tile.openstreetmap.org`. |
| 10 | **T7 kurs wg daty** | Polityka `fx_rate_basis` na opłacie (ETD / załadunek / D-1); przeliczenie w SQL. | Ustawa o VAT art. 31a; M-23 już jest. | LLM/JS nie liczą. |
| 11 | **D1–D3 drobnica** | Linie+cutoff+TT; przesyłka/paczka 4 poziomy + skan; cross-dock/awizacje. | Siła SPEED (dossier 37 źródeł); iSPEED dopiero XI 2025. | Nie pełny WMS. Nie optymalizator. |
| 12 | **D9 silnik wydruków** | Szablon = dane; wymóg sieci przed wyjazdem (409 jak C8); CMR / groupage / SSCC / ZPL; QR `shipment_ref` na każdym druku. | Qargo help: brak etykiety = ładunek nie wejdzie na hub. SPEED: walidacja skanu wg trasy/statusu. | Bez kodu Omni = HITL. M-38 dziś bez bajtów. |
| 13 | **D8 sieci 1./ostatnia mila** | Etykieta sieci po **oficjalnym** API; import do systemu sieci gdy API nie ma. | Qargo sam odsyła Palletforce/Alliance do systemu sieci. | **TO_VERIFY API** — bez umowy nie kodować generatora obcej etykiety. |
| 14 | **P1–P4 cennik jako dane** | Rate card WHEN/IF/CALC/MIN/MAX; szablony opłat; FSC/indeks; Local Charge Library + warning braków. | SPEED: cenniki = ręczne T-SQL; ROHLIG SUUS ~rok poślizgu; Rhenus „łzy”. Funkcja zostaje, mechanizm T-SQL odrzucony. | Matching w SQL. Warning ≠ fakt. Marża zostaje w `charge`. |
| 15 | **P5 expected vs actual** | Snapshot kosztu tripa przy `in_transit` + wariancja. | Qargo Knowledge Hub: expected vs actual. | Nie druga marża. |
| 16 | **X1–X2 portale** | Klient: zlecenia/T&T/dokumenty. Przewoźnik: trip, taski, POD, self-billing. | Najlepiej sprzedające się u Qargo: driver app + fakturowanie z FK. S55 w kanonie = ogólnik F10; X = konkret. | **Po Auth0 S53.** `/noc` i tak pomija S53/S55. |
| 17 | **X3 + X4** | Apka kierowcy = poziom 0 GPS na czas zlecenia. Webhooki + **pierwszy konsument outboxa**. | Konsument = warunek zdjęcia „nie Temporal na zapas”. | Zgoda kierowcy. S59 OTel parked aż konsument/umowa SaaS. |
| 18 | **X7 lejek oferty** | `sent` / `pdf_viewed` / `replied` / `converted`; czasy w SQL; hostowany PDF z tokenem. | Diagnostyka: nie otworzył vs otworzył i nie odpisał vs odrzucił cenę. Mailto bez Graph: załącznik nie da sygnału — link PDF jest sygnałem. | Piksel tylko po zgodzie. `email_opened` niska pewność (Apple Mail Privacy). |
| 19 | **X9 + X6 skan** | Gate + OpenCV (kadr, cień, biel, ~300 DPI Lanczos) + bbox/pewność + split HITL; diff CMR/POD vs zlecenie. | Qargo Document Intelligence; Photo POD „zrób ponownie”. Dziś M-20 split bez bbox i enhance. | Nie GAN. Kwota z `amount_text` przy accept. Optimistic accept zakazany. |
| 20 | **F1 KSeF live** | FA(3), tryby, QR — Omni wystawia. | **Mandat PL już w mocy 2026** (kalendarz regulacyjny matrycy). Dziś S35 = numer sesji, nie live HTTP. | Nie KSeF z ERP. |
| 21 | **F9 + F10** | Adapter FK: FS+FZ do Comarch/Symfonia/Subiekt. Ingest FV kosztowej mail/KSeF XML/skan → ranking SQL → HITL. | Operator 2026-09-07: Omni wystawia, ERP nie liczy marży. XML FA(3) bez LLM. | Agent outbound, nie SQL do bazy klienta. Nigdy auto-link. |
| 22 | **F11 książka nadawcza** | `paper_post` → `postal_dispatch` + EN + śledzenie + EPO. Bez nadania ≠ „wysłana”. | Dwa oficjalne API PP (EN SOAP w96 + REST `checkmailex`), spec publiczne IX 2026. Max 500 w kopercie EN. | Papier ≠ wyłączenie KSeF. Imię odbiorcy tylko EPO. |
| 23 | **C1 + C7 + C8** | SENT+GEO; katalog `monitoring_scheme` (nie mit „SENT w każdym kraju”); `party_document` blokuje `POST shipment` (polisa/składka/licencja). | P0: SENT, EKAER, RO e-Transport, BDO, DIWASS gdy API. WSR 2024/1157 od 21.05.2026. | Brak klona SENT w SK/CZ/AT/NL/BE/… — nie wymyślać. Nie scoring osoby. |
| 24 | **C9 snapshot Trans.eu** | `overall_rating`, satisfaction, TransRisk, `documents.expire_date` po partners-api. | Oficjalne API potwierdzone IX 2026. Próg blokady = M-03. | Opinie słowne: **brak** publicznego endpointu — nie scrapować. |
| 25 | **V5 hub + V6 wieża** | `PositionEvent`; L0 / L1a Teltonika+Queclink (`omni_telematic` = flota w umowie) / L1b BYO / L1c. External: 3 dni robocze bez trip, nowy trip włącza. Wieża: stock→EBITDA. | Qargo bez wieży załadowcy. SPEED bez predykcji. Art. 5: minimalizacja na external. | **Nie noc.** Zero własnego HW. AIS ≠ V5. |

---

## B. Do doprecyzowania / TO_VERIFY — bez tego nie wolno kodować

Brak API, umowy albo podstawy prawnej = park, nie teatr HTTP. Statusy prawdy ADR-0004: CONFIRMED / TO_VERIFY / PROPOSAL.

| # | Temat | Czego brakuje | Skutek jeśli kod bez tego |
|---|---|---|---|
| 1 | **Auth0 / tenant (S53)** | Tenant produkcyjny. PLAN: I1/I2 nie teraz; hello JWT zostaje. | Portale X1/X2 i S55 bez IdP = atrapa logowania. |
| 2 | **S21 kanały armatorskie** | Umowa. Park w kanonie. | Live HTTP bez kontraktu = teatr. |
| 3 | **D8 etykiety sieci** | Oficjalne API Raben / Schenker / Hellmann / Palletforce / Alliance. | Udawany generator etykiet — odrzucone na stałe. |
| 4 | **V5b giełdy tracking** | Umowa na Trans.eu `transports/{id}/monitoring`+`/trace`; TIMOCOM Shipment Tracking; Transporeon Open Visibility. | Poll cudzej floty bez prawa do danych. Teleroute API = CRUD ofert, **nie** GPS. |
| 5 | **Czat giełd (własny tenant)** | Trans.eu: brak publicznego API historii messengera (IX 2026). TIMOCOM: zapowiadany eksport do pliku — TO_VERIFY. | Kod „czytający czat” bez API = scraping (lista C). |
| 6 | **Opinie słowne Trans.eu** | Publicznego endpointu komentarzy nie ma; pytać `api@trans.eu`. | Scraping profili odrzucony. Wolno: scoring z partners-api. |
| 7 | **L1c aggregator** | Umowa i cennik Linkway INTEGRATOR / DRIP. | Hub „230/400 platform” bez kontraktu = obietnica. |
| 8 | **L1a Teltonika/Queclink** | Protokół **per model** (wiki producenta). | Adapter zgadujący ramkę. |
| 9 | **Native GPS poza P0** | P0 analizy: GBOX, IKOL, Flotis, Wialon (docs publiczne). Reszta PL/EU: dokumentacja + umowa. Tronik ATRAX4 / Logisat: swagger niepubliczny. | Native adapter bez docs zakazany; do tego czasu aggregator. |
| 10 | **Berg Insight / Geotab** | Geotab po zakupie Verizon Connect EU (2025, poza ES) — ranking przy implementacji TO_VERIFY. | Zła kolejność adapterów ≠ błąd prawny, ale zły P0. |
| 11 | **PUESC C2** | Dostęp AIS-IMPORT / AES / Intrastat (konto, środowisko test). | Formularz „celny” bez urzędu. |
| 12 | **Katalog SENT-europa** | GR ICSISnet zakres; BG e-Transport ustawa+API. Reszta krajów: brak klona = brak adaptera. | Fałszywa zgodność (lista C). |
| 13 | **BDO API 1.01.2027** | Nowa spec MOS; dziś swagger test-bdo.mos.gov.pl. | Adapter pod stary kontrakt padnie w dniu zmiany. |
| 14 | **DIWASS** | API KE dla oprogramowania komercyjnego (IR 2025/1290) — czy tenant/integrator ma dostęp. | Flaga odpadu bez zgłoszenia transgranicy. |
| 15 | **Myto EU/EFTA** | Wybór: PTV / NAPSPAN / TollCalc (~37 krajów) vs taryfy publiczne (e-TOLL, Toll Collect, ASFINAG…). Brak jednego darmowego API UE. | Zmyślona kwota myta = zakaz; brak taryfy = warning. |
| 16 | **Nakordoni Truck Bans / Carto / Esri tiles** | Licencja i atrybucja przy implementacji. | TOS jak OSMF na `tile.openstreetmap.org`. |
| 17 | **X7 klik PDF** | Prawnik: wykonanie umowy vs uzasadniony interes vs zgoda (EDPB 2/2023, CNIL IV 2026, PKE). Piksel: zgoda **osobna**. | Tracking oferty bez podstawy. |
| 18 | **`delivered` maila** | DSN / Graph delivery — per skrzynka często brak. | Metryka „doręczono” z powietrza. |
| 19 | **EN + EPO (F11)** | Umowa biznesowa PP + usługa EPO na przesyłce. REST śledzenia **nie** zwraca imienia. | Obietnica „kto odebrał” bez EPO. |
| 20 | **ERP P0 licencje** | Comarch XL: CDN API / licencja partner. Subiekt: Sfera (nexo PRO vs dokupić; GT ≠ nexo). Symfonia: klucz aplikacji WebAPI. | Surowy SQL do MSSQL klienta = odrzucone. |
| 21 | **F5 diety / F7 faktoring** | Stawki per kraj; partner faktoringu. | Kwoty diet z LLM / workflow bez wypłaty. |
| 22 | **V7 tacho / posting / art. 9 promu** | Prawo per kraj; apka **nie** poprawia tachografu. | „Wolno/nie wolno” od modelu. |
| 23 | **HZ konektory** | Booking armatorski per carrier; Baltic Hub OAuth2; BCT/GCT B2B; promy API; P&O Freight od 1.06.2026 (stare EDI nie). | HTTP na zgadywanych URL. |
| 24 | **Chłodnie zdalne** | API **per urządzenie**. | Sterowanie bez kontraktu. |
| 25 | **Scanbot / cloud DI** | Licencja SDK; cloud tylko BYO (HC-05). OpenCV+ML Kit/VisionKit = P0 bez tej licencji. | Płatny skaner jako ukryty wymóg. |

Umowy wywiadowni (KRD/Coface/D&B/CreditSafe) i giełdowe market data (Transporeon Insights) też TO_VERIFY — HZ, nie P0 tej listy.

---

## C. Odrzucone — pozycja + argument + data/źródło

„Odrzucone na stałe” ≠ „odroczone → HZ”. Drugie może wrócić po decyzji; pierwsze nie wchodzi do kodu.

| # | Pozycja | Argument | Status |
|---|---|---|---|
| 1 | Rewrite Django / GraphQL / Apollo / Zustand / Ant / Linaria | Zero zysku domenowego; utrata 128 plastrów z RLS/testami; sprzeczne z ADR-0002. | **Na stałe** — ADR-0004 2026-09-07 |
| 2 | Klon Qargo 1:1 | Qargo = road-first, bez KSeF/SENT/białej listy, bez control tower załadowcy. | **Na stałe** — ADR-0004 |
| 3 | 200 modułów bez warstwy stop/trip/zasób | Zlecenie bez wykonania nie domyka jobu spedytora. | **Na stałe** (kolejność) — ADR-0004 |
| 4 | Cenniki / wydruki jako ręczne T-SQL (mechanizm SPEED) | Każde wdrożenie = dialekt; ostrzega instrukcja producenta. Funkcja (rate card, szablon) wchodzi jako dane. | **Mechanizm na stałe**; funkcja w A |
| 5 | Kod, branding, assety, teksty docs Qargo/SPEED | Prawo autorskie. | **Na stałe** |
| 6 | **Wyłącznie** zautomatyzowana decyzja kredytowa / HR bez człowieka | Art. 22 + AI Act. **2026-09-08:** szkic AI + umowy RODO **wolno**; zapis limitu / score osoby tylko po S11. | **Na stałe: auto-decyzja.** Sugestia = kanon M14b |
| 7 | B2C / osoby prywatne bez NIP | Decyzja operatora **2026-09-07**; M10-1 odmawia zapisu. | **Na stałe (biznes)** |
| 8 | BIK / systemy bankowe | Decyzja operatora **2026-09-07**. Zostają KRD (BIG), Coface, D&B, CreditSafe, rejestry jawne. | **Odrzucone (decyzja)** |
| 9 | Własne urządzenia GPS (projekt / produkcja / firmware) | Decyzja operatora **2026-09-07**. HW = Teltonika+Queclink u przewoźnika, który chce pakiet. | **Na stałe (biznes)** |
| 10 | Poll floty na **zewnętrznym** GPS poza 3 dniami roboczymi | Art. 5. **2026-09-08:** `omni_telematic` (pakiet Omni + umowa) = flota OK; external = 3 dni robocze, nowy trip włącza. | **Na stałe tylko external poza oknem** |
| 11 | Scraping WCA / giełd / terminali / śledzenia PP / Envelo | ToS + prawo; PP ma REST/EN; NIS2. | **Na stałe** |
| 12 | Podsłuch / scraping czatów giełd, gdy tenant nie jest stroną | Art. 267 KK + RODO + ToS. Brak publicznego API historii czatu (IX 2026). | **Na stałe (prawo)** |
| 13 | Wymyślanie narodowych „SENT-ów” | Większość UE nie ma klona. Katalog tylko ze źródłem prawnym. | **Na stałe** |
| 14 | Scraping opinii słownych Trans.eu / TIMOCOM | Brak publicznego API komentarzy (IX 2026). | **Na stałe** |
| 15 | Niewidoczny piksel / tracker 3rd party / tracking osób prywatnych | ePrivacy; EDPB 2/2023; PKE; CNIL 2026. | **Na stałe (prawo)** |
| 16 | RAG / pgvector na wycenie, VAT, schemacie DB | HC-08. | **Na stałe (HC)** |
| 17 | `tile.openstreetmap.org` jako CDN produkcyjny | Polityka OSMF: serwer społecznościowy ≠ CDN aplikacji. | **Na stałe** |
| 18 | HERE jako **baza** map/telematyki | PDF s.66: licencja asset-management. Premium BYO OK. | **Odrzucone jako podstawa** |
| 19 | Auto-zlecenie / auto-`charge` z maila albo geofence; auto-link FV; auto-link skanu bez QR Omni; accept bo „pewność wysoka” | HC-04 + ADR-0003. Propozycja tak, zapis po człowieku. | **Na stałe** |
| 20 | Real-ESRGAN / GFPGAN / inpainting glifów na FV/CMR/cenniku | Dopowiada cyfry. Enhance = OpenCV, DPI = Lanczos. | **Na stałe** |
| 21 | Udawany generator etykiet Palletforce/Alliance | Qargo też odsyła do systemu sieci. | **Na stałe** |
| 22 | Podwójny KSeF (Omni + ERP); ERP nadpisuje `charge` | Decyzja **2026-09-07**: wystawia wyłącznie Omni. HC-03. | **Na stałe** |
| 23 | Surowy SQL / `sa` do Comarch/Subiekt/Symfonia | Omija Sferę/CDN/WebAPI. | **Na stałe** |
| 24 | Gwarancja „kto odebrał” przy papierowym ZPO bez EPO | REST PP nie ma imienia; imię = `getEPOStatus` albo HITL ze skanu. | **Odrzucone jako gwarancja** |
| 25 | Dwa produkty (Super TMS + osobny enterprise); 200 silosów; „AI przewiduje”; „100% zgodność prawna”; SLA „oferta w 8 min” / „wdrożenie w 4 h”; Temporal/Hatchet na zapas | Jeden core, dwie perspektywy. Skuteczność = Prediction Ledger. Outbox consumer najpierw (X4). Copy mockupu ≠ DoD. | **Na stałe / warunek** — rejestr + ADR |

**Odroczone (HZ, nie „nie”):** WhatsApp; Energy Intelligence; mikroserwisy; Connected Carrier / finansowanie GPS (HW własny i tak odrzucony); digital twins pełne; war room; autonomous negotiation (tylko z limitami+HITL); e-Doręczenia ≠ książka PP.

**Świadome POMIŃ (funkcja ≠ mechanizm):** stack Qargo; T-SQL; polskie nazwy kolumn w bazie; drugi grid engine.

---

## Jak czytać tę kartę przy decyzji

1. **Przypięcie fali (2026-09-08):** PLAN § Kolejka + CURRENT wskazują P0 → Fala O → Fala I → T/D/P/X/F/C/V. Named parks parked. `/noc` nie startuje sam z pinu.
2. **Named parks kanonu** (S53 Auth0, S55 portale, AIS leftover, S50/S54/S59/S21) zostają, aż operator zmieni kanon albo pojawi się tenant/umowa/job.
3. Pozycja z listy B wpinana do kodu bez źródła = błąd blokujący, nie „zrobimy adapter”.
4. Karty pól — wejście do `/plan-modul` (ADR-0004), nie skrót z tej karty.
