# Stan planu — inwentarz decyzji (pola, funkcje, UI, integracje, AI)

**To jest Markdown w repozytorium.** Nie canvas. Inwentarz decyzji; **kolejka kanonu** od 2026-09-08 = [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) (P0 + Fala O + Fala I + T/D/P/X/F/C/V). Named parks parked.  
**Data:** 2026-09-08.

**Uczciwość.** Ten plik **nie** pokrywa 376 stron PDF 1:1 i **nie** jest 324 kolumnami pól jako osobne wiersze. Pokrywa **inwentarz warstw** plus **wiersze funkcji**. Tally: katalog pól **324 / 32** (+ tabele O/B0/M10 w kartach i pola-wizja). Dostępy **49** checkboxów. Tabele 1–4 = 47 / 25 / 37 / 35. Fale T–V **są w kanonie kolejki** (pin 2026-09-08); `/noc` nie startuje w sesji pinu. Ziarno 42 z PDF: **0** silników poza matrycą ([luki-pdf-vs-stan.md](luki-pdf-vs-stan.md)).

---

## Werdykt o canvasie

**NIE — canvas nie jest dokumentem, o który prosił operator.**

Plik `wizja-plan-decyzja.canvas.tsx` otwiera się w panelu Canvas Cursora na Windows, nie jako zwykły plik Markdown w repo. To dashboard: siedem zakładek (Werdykt, Wcielamy, PDF §13q, AI, API vs umowa, Do doprecyzowania, Odrzucamy) i kafelki `Stat` (18/5/0, 36/10, 324/32/49). Żadna z czterech wymaganych tabel — Zaplanowane w 100% / Niezaplanowane z rozmowy i PDF / Wymaga weryfikacji / Odrzucamy — nie ma kolumn `Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status` na każdą funkcję. Makiety UI do decyzji: [ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx) (HITL Art. 50) i [ui-06-vision.canvas.tsx](../design/ui-06-vision.canvas.tsx) (wieża) — osobne od tego dashboardu. Operator z otwartym `dostepy-do-zdobycia.md` potrzebuje tego pliku MD, nie panelu Canvas.

---

## Tabela podsumowania

| Co | Wynik |
|---|---|
| Rozmowa vs **matryca** | 23 tematy z listy operatora: **18 WCIELEONE**, **5 CZĘŚĆ**, **0 BRAK** w matrycy. Źródło: [audyt-rozmowa-vs-plan.md](audyt-rozmowa-vs-plan.md). To audyt matrycy, **nie** audyt kolumny Funkcja. |
| Rozmowa vs **wiersze** | [luki-rozmowa-vs-stan.md](luki-rozmowa-vs-stan.md): **75** tematów bez własnego wiersza w tabelach 1–4 (w tym Select & Drop, Pre-planning, mapa 1000+polygon, markery, Satellite/Traffic/Truck Restrictions). Uzupełnione: Inwentarz warstw + tabela 5. |
| PDF ChatGPT vs matryca | Audyt: **42** nazwane silniki poza ówczesną matrycą. **Nie wiszą poza planem.** Zamknięcie: **36** wierszy §13q + **10** w rejestrze. 36+10=46 przez rozszczepienia. Źródło: [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md). |
| PDF vs **wiersze** | [luki-pdf-vs-stan.md](luki-pdf-vs-stan.md): **136** nazw bez wiersza w tabelach 1–4; **28** to aliasy istniejących wierszy (nazwa dopisana poniżej). Ziarno 42: **0** poza matrycą. |
| Pola | Katalog [pola-wizja-2026-09.md](pola-wizja-2026-09.md): **324** wiersze + dopiski O (`transit_days`, `party_lane_scorecard`, `party_id` na członku). Karty kolumn: T, O, P, D, X, F, C, V. |
| `charge.source_ref` | Tabeli `charge` **brak** kolumny `source_ref` (buy/sell są). To **P0 — następny** w PLAN/CURRENT. V2b i F11 tego wymagają. |
| Dostępy | **49** checkboxów `### - [ ]` w [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md). Lista **nazw P0**: Inwentarz warstw · Integracje. Spec publiczna = wolno pisać klienta; live i tak na sekretach tenanta (HC-05). Zakaz scrapingu. |
| Kanon vs analiza | **Kanon** (`CURRENT.md`, 2026-09-08): Etap Plan, **P0** potem **Fala O + I**. Named parks parked. Fale T–V w PLAN. Karty: `karty-pol-fala-o.md` / `i.md` … `v.md`. Audyt Incoterms: `incoterms-booking-customs-ux.md`. |
| AI | **TAK** tylko HITL extract (szkic): DocILE LayoutLMv3 KILE F1 **0,698**, LIR F1 **0,721** — residual ~30% pól. **NIE** autonomiczny zapis (Goddard RR **1,26**; Skitka commission **3,92/6**, dokładność 35%). **NIE** LLM jako kalkulator (PAL GSM-HARD CoT **20,1%**). **NIE** GAN na FV. **NIE** scoring osoby/JDG. Trzy **tabele jobów** (listy 1/2/3): Inwentarz warstw · AI. Źródło: [ai-nauka-i-dowody.md](ai-nauka-i-dowody.md), [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md). |

---

## Inwentarz warstw

Warstwy nie zastępują tabel 1–4. Kolumny pól: [pola-wizja-2026-09.md](pola-wizja-2026-09.md). Checkboxy dostępów: [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md). Job AI: [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md). `container` (T3) jest w tabeli 1 funkcji i **nie** jest na liście 32 — nadmiar wobec katalogu pól, nie luka.

### 32 tabele (nazwy; nie 324 kolumny)

Kolumny każdej tabeli są w [pola-wizja-2026-09.md](pola-wizja-2026-09.md) § „NOWE (brak tabeli)” pozycje 1–32. Dziewięć nazw było już w tabelach funkcji (nie jako inwentarz pól): `stop`, `trip`, `resource`, `entity_event`, `position_event`, `exchange_message`, `monitoring_scheme`, `party_document`, `postal_dispatch`.

| # | Tabela | Co to |
|---|---|---|
| 1 | `relation_document_requirement` | Wymagany zestaw `party_document` per relacja (krajowa / międzynarodowa / odpad); 409 na `POST shipment`. Nie scoring osoby. |
| 2 | `resource` | Płyta / kierowca / naczepa (`kind`). Myto czyta klasę i osie stąd. |
| 3 | `trip` | Jednostka wykonawczo-kosztowa; start/stop okna GPS. |
| 4 | `stop` | Punkt ZA/WY/cło/prom/terminal z oknem i statusem. |
| 5 | `position_event` | Kontrakt PositionEvent: GPS z adapterów. Nie `tracking_event`. |
| 6 | `telematics_connector` | Adapter + sekrety BYO (ciphertext kluczem tenanta). |
| 7 | `resource_telematics_link` | Wiązanie płyty z kontem GPS; `observation_status` idle/active/grace/stopped. |
| 8 | `exchange_message` | Wiadomość giełdy tylko gdy tenant jest stroną. Zakaz scrapingu. |
| 9 | `entity_event` | Szyna B0 append-only (metryki jobu, pogoda jako czynnik, nie liczba z LLM). |
| 10 | `weather_observation` | Open-Meteo (i suplement) wzdłuż geometrii `trip`, nie jeden kraj załadunku. |
| 11 | `party_document` | Polisa / licencja / BDO; niemutowalna historia; odblokowanie = nowy wiersz. |
| 12 | `party_exchange_snapshot` | Snapshot Trans.eu Partners. Nie mylić z `party_scorecard`. |
| 13 | `monitoring_scheme` | Katalog SENT-EU per tenant. Brak klona w kraju ≠ wymyślony wiersz. |
| 14 | `shipment_monitoring_filing` | Numery i statusy zgłoszenia SENT/BDO na zleceniu. Omni nie zastępuje urzędu. |
| 15 | `map_basemap` | Katalog podkładów jako dane; `is_blocked` na `tile.openstreetmap.org`. |
| 16 | `user_map_prefs` | On/off warstw u usera. Bez kluczy API. `table_view` zostaje na siatki. |
| 17 | `tenant_map_provider` | Płatne BYO u admina (klucz tenanta, ograniczenie domeny). |
| 18 | `erp_connector` | Konto adaptera FK: Optima / XL / Symfonia / nexo / GT. Agent outbound. |
| 19 | `erp_series_map` | HITL pierwszego mapowania serii FS/FZ. Adapter nie liczy marży. |
| 20 | `erp_export` | Status eksportu do ERP. Bez nadpisu kwot Omni. |
| 21 | `scan_enhance_run` | Metadane OpenCV (warp/deskew/biel). Oryginał zostaje. Zakaz GAN. |
| 22 | `invoice_match_candidate` | Drabina SQL match FV kosztowej. Score liczy SQL, nigdy auto-link. |
| 23 | `network_print_requirement` | 409 bez etykiety sieci; odblokowanie = wydruk + `source_ref`. |
| 24 | `document_template` | Szablon wydruku jako dane. Nie `quotation_print_template` (token M-03). |
| 25 | `shipment_package` | Segment QR: tenant + shipment + package + `document_kind`. |
| 26 | `postal_dispatch` | Jedna przesyłka PP; klucz = `numer_nadania`. |
| 27 | `postal_tracking_event` | Zdarzenia REST USS / EN. Upsert po numerze + kod + czas. |
| 28 | `postal_epo` | Imię odbiorcy (`getEPOStatus`). PII; tylko umowa EPO. Nie w promptach. |
| 29 | `purchase_invoice` | FV kosztowa. Bez HITL accept nie wchodzi na zlecenie. |
| 30 | `purchase_invoice_allocation` | Jedna FZ → wiele zleceń. Suma linii = kwota FV (**SQL**). |
| 31 | `quote_engagement` | Lejek oferty append-only (`sent` / `pdf_viewed` / `delivered` / `lost` / …). Czasy = SQL. |
| 32 | `quote_view_token` | Token hostowanego PDF. Załącznik mailto nie trackuje. |

**32/32 nazw wizji wieczornej.** Pin 2026-09-08 dodał: `party_lane_scorecard`, `party_role_assignment`, `prediction_ledger`, `plan_snapshot` (karty O/P/V). Rozszerzenia istniejących (`shipment.shipment_ref`, `charge.source_ref`, `draft_kind` w tym `carrier_quote`, `network_member.party_id`, `channel_quote.transit_days`, …) są w pola-wizja § „Rozszerzenie”.

### Powierzchnie UI

T6 ≠ X8. V6 ≠ V5. X9 split ≠ X6 diff. Makiety: [docs/design/README.md](../design/README.md), [ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx), [ui-06-vision.canvas.tsx](../design/ui-06-vision.canvas.tsx). Kolejka propozycji T6 / X7 / X8 / V6 **nie** jest kanonem PLAN.

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Select & Drop | Wiele zleceń → zasób z walidacjami ładowność / ADR / okna / marża | Board T6 bez tego = tylko cztery layouty | LLM nie waliduje. Marża zostaje w `charge` | rozmowa #1; matryca §2; kolejka T6 | analiza · nie kanon |
| Lazy map (1000 + polygon) | Selekcja na mapie do ~1000 zleceń: rectangle/polygon; mapa **lazy**, nie initial 250 kB | T6+X8 w tabeli 1 milczy o 1000 i polygon | Paczka JS: mapa poza budżetem initial | rozmowa #3; matryca §2 | analiza · nie kanon |
| Pre-planning | Przestrzeń przed przypisaniem zasobu (parkowanie zleceń) | Osobny stan niż `trip.assigned` | Nie auto-assign (osobny wiersz) | rozmowa #2; matryca §2; kolejka T6 | analiza · nie kanon |
| Katalog podkładów i nakładek (Satellite / Live Traffic / Truck Restrictions) | `map_basemap` + overlay: satelita, ruch live, restrykcje TIR / LEZ / ORM; darmowe on/off u usera, płatne BYO u admina | P0 OpenFreeMap + GUGiK na powierzchni mapy | Zakaz `tile.openstreetmap.org`. Nakładki Parking/Fuel w tabeli 2 ≠ ten katalog | rozmowa #5; §13k; [podklady-map-admin.md](podklady-map-admin.md) | analiza · nie kanon |
| Lejek quote `delivered` / `lost` | Widok szczebli + czasy SQL; zdarzenia poza `sent`/`pdf_viewed`/`replied`/`converted`: `email_opened`, `delivered`, `lost` | Tabela 1 X7 ma cztery stany, nie ten widok | `email_opened` niska pewność (Apple MPP). `delivered` = B#18 | rozmowa; kolejka X7; `quote_engagement` | analiza · nie kanon |
| Wieża: stock → produkcja → sprzedaż → EBITDA + „co jeśli” | Łańcuch wieży; „co jeśli nie zareagujesz”; canvas ui-06 (Watchtower / oś / portale) | V5+V6 w tabeli 1 = jedno zdanie. Early Warning GREEN/AMBER/RED/BLACK jest w tabeli 2 jako HZ, nie jako UI V6 | Nie scoring osoby. Nie kanon nocy | rozmowa; kolejka V6; ui-06-vision | analiza · nie kanon |
| **ui-04** HITL (Art. 50) | Makieta [ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx): label Art. 50 zawsze widoczny; pewność per pole; próg 0,7 + disambiguation; accept zbiorczy tylko zaznaczonych; odrzucenie z uzasadnieniem; optimistic accept zakazany; spany na PDF | Zero wystąpień `ui-04` w starym stan-planu | Kod: split bez pewności per pole. `U-art50` = leftover UI | luki-warstwy; PLAN `U-art50`; ADR-0003 | analiza · luka UI vs kod |
| Split HITL X9 | Jeden ekran: lewo dokument / prawo wartość + rodzaj + pewność + edycja. `draft.kind` różni job (RFQ / FV / cennik / CMR), nie nowy ekran. Istnieje `hitl-review-split.tsx` | X9+X6 w tabeli 1 = „bbox + split”, nie kontrakt UI | Nie drugi split na kind | rozmowa #35; §13o; karta 010 | analiza · nie kanon |

### Integracje P0 (nazwy)

Checkboxy i „co zrobić”: [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md) (49 pozycji). Tu **nazwy**, nie tally. **P0** = linia „P0 = …” w dostępy + nagłówki `###` z **P0**. VisionKit jest parą on-device z ML Kit (nie zawsze tag P0 w nagłówku).

| Nazwa | Co to | Blokuje kod? | Gdzie indziej w tym pliku |
|---|---|---|---|
| OpenFreeMap | Darmowy podkład wektorowy; komercja dozwolona; brak SLA | NIE | UI X8; B#16 / C#17 |
| GUGiK WMTS | Orto + topo PL, bez klucza | NIE | UI X8; B#16 |
| Google ML Kit Document Scanner | Android on-device; FV: `BASE_WITH_FILTER`; `FULL` nie na kwocie | NIE | tabela 5 X9-capture |
| Apple VisionKit | iOS `VNDocumentCameraViewController`; ten sam pipeline pliku | NIE | tabela 5 X9-capture |
| Comarch ERP Optima | SOAP/WebAPI + agent; FS+FZ | TAK (kit partnera) | F9 rozklejone |
| Comarch ERP XL (CDN API) | Inny adapter niż Optima; CDN_API.DLL | TAK | F9 rozklejone |
| Symfonia WebAPI | REST/JSON; docs publiczne | NIE (kontrakt); live = klucz tenanta | F9 rozklejone |
| Subiekt nexo (Sfera) | COM; nie publiczny REST | TAK | F9 rozklejone |
| Subiekt GT (Sfera GT) | Inny dodatek niż nexo | TAK | F9 rozklejone |
| Palletforce Alliance API | Etykieta sieci 1:1. Nie udawany generator | TAK | D8 w tabeli 3; C#21 |
| Poczta REST USS 2.0 | Śledzenie po `numer_nadania`. Imienia w REST **nie ma** | NIE | F11; osobny kanał vs EN SOAP vs EPO |
| GBOX (Inelo) | Native GPS P0 PL | TAK (docs.gbox.pl za loginem) | V5 rozklejone |
| IKOL | Native GPS; docs publiczne | NIE | V5 rozklejone |
| Flotis REST | Native GPS; docs publiczne | NIE | V5 rozklejone |
| Wialon SDK | Native GPS; docs publiczne | NIE | V5 rozklejone |
| Open-Meteo | Pogoda pan-EU wzdłuż trasy | NIE; SaaS = płatny plan albo AGPL | V2 tabela 1 |
| KSeF API 2.0 | Omni wystawia FA(3) | NIE | F1 tabela 1 |
| BDO REST | KPO; zmiana API 1.01.2027 | NIE wobec swaggera | C6 tabela 1 |
| SENT PUESC | Zgłoszenia XML; nie „SENT-Europa” | NIE (XSD); live po koncie | C1 tabela 1 |
| Trans.eu Partners | Snapshot scoringu / dokumentów | NIE wobec JSON; live po kluczach | C9 tabela 1 |
| Trans.eu monitoring/trace | GPS zadania, nie całej floty | NIE (docs) | V5b tabela 1 |
| Elektroniczny Nadawca SOAP w96 | Książka nadawcza; max 500 | NIE wobec PDF; live po umowie | F11 tabela 1 |
| EPO `getEPOStatus` | Imię odbiorcy | NIE (opis); live bez umowy EPO = puste imię | F11; C#24 |

Reszta checkboxów (IMGW/DWD/Météo-France, EKAER, RO e-Transport, DIWASS, TIMOCOM, Transporeon, Teltonika, Queclink, Linkway, DRIP, PTV/HERE/NAPSPAN/TollCalc, Palletline, Carto, Esri, …): [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md). Nie dump 49 wierszy „co zrobić” tutaj.

### AI — trzy tabele jobów

Źródło i uzasadnienie: [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md). To **joby**, nie akapit zasad. Lista 2 nie idzie do „zaplanowane”; pokrywa się z tabelą 4 tam, gdzie już jest odrzut.

#### Lista 1 — AI TAK (HITL obowiązkowy)

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Cennik/oferta → `amount_text` | Kandydaci stawek + `charge_code` z katalogu + `unparsed_regions` | Zero transkrypcji cennika | Accept → `rate_line` w tym samym HTTP; `ExtractionService` nie zapisuje stawek | ai-gdzie §1 #1; M-20 | AI TAK · HITL |
| `inbound_message` → `extract_to_draft` | Treść / załącznik tym samym kanałem | Jeden extractor, nie drugi | HITL zostaje | ai-gdzie §1 #2 | AI TAK · HITL |
| Mail → szkic RFQ (Email Intelligence) | Klasyfikacja + ekstrakcja pól zlecenia, nie silnik wyceny | Mniej kopiowania z wątku | Matching `party` nie jest auto-zapisem. Ocean Email AI w tabeli 2 = inny job (armator) | ai-gdzie §1 #3; rozmowa #7 | AI TAK · HITL |
| FV kosztowa → `draft.kind=purchase_invoice` | Mail / skan → `extraction_draft` | Jedna kolejka zamiast ręcznego FZ | Bez accept brak `purchase_invoice` i brak sync FK | ai-gdzie §1 #4; §13m | AI TAK · HITL |
| Skan CMR/POD bez kodu Omni | Kind + pola gdy brak QR Omni | Operator nie zgaduje zlecenia z rozmazanego CMR | Model nie wybiera `shipment`; drabina SQL + accept | ai-gdzie §1 #5; §13n tor 2 | AI TAK · HITL |
| Jeden split HITL, `draft.kind` różni job | RFQ / FV / cennik / CMR na jednym UI | Nie pięć ekranów | Confidence per pole, span/bbox, reject z powodem, Art. 50 | ai-gdzie §1 #6; ui-04 | AI TAK · HITL |
| `bbox` + pewność 0–1 + `span_text` + `operator_override` | Pola kandydata w JSONB; edycja `amount_text` przed accept | Niskie pasmo nie wchodzi w accept zbiorczy | Decimal przy accept w kodzie; override nie „poprawia” pewności modelu | ai-gdzie §1 #7; rozmowa #36 | AI TAK · HITL |
| Klasyfikacja `document_kind` gdy brak QR | Porządek skrzynki skanów | D9: HITL bez kodu ≠ ta klasyfikacja | Zapis `shipment_document` po accept (tor bez kodu) | ai-gdzie §1 #8 | AI TAK · HITL |
| Diff pól vs zlecenie (X6) | Waga / sztuki / data: widać rozjazd | Nie cichy overwrite | Konflikty do recenzji. X6 ≠ X9 | ai-gdzie §1 #9 | AI TAK · HITL |
| `mail_draft` „podaj `shipment_ref` / kontener” | Szkic maila przy FV bez sygnałów | Mniej ręcznych maili o numer | Świadomy mailto; nigdy auto-send | ai-gdzie §1 #10; §13m | AI TAK · HITL |
| Label Art. 50 / `U-art50` | „Propozycja AI” zawsze na szkicu | Spełnienie Art. 50 w UI (ui-04) | Draft bez labelu = gate pada. D0 nie zdejmuje HITL | ai-gdzie §1 #11; PLAN U-art50 | AI TAK · HITL |
| Guard regex; llm-guard + Presidio = cel HC | Wejście niezaufane nie idzie nagie do LLM | Guard ≠ zapis | CI = `mock`. Żywy llm-guard to cel HC, nie runtime dziś | ai-gdzie §1 #12; AGENTS | AI TAK · HITL |

OpenCV kadr/enhance i ML Kit / VisionKit to **geometria przed** instructorem, nie wiersz listy 1.

#### Lista 2 — AI NIE

| Funkcja | Co robi (zakaz) | Plus (zostaje) | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Sumy / marża / VAT / kurs w modelu | Model nigdy nie liczy | `charge.margin` i SQL | HC-02, zasada 4 | ai-gdzie §2 #1 | AI NIE · HC |
| Auto-zapis extractu / `rate_line` / `charge` | AI = JSON/intent; zapis = `service` po człowieku | Propozycja tak | HC-04; C#19 | ai-gdzie §2 #2 | AI NIE · HC |
| Sell / marża z LLM | LLM nie wstawia sprzedaży | Accept HITL ≠ `charge` | HC-03; C#22 przy T4 | ai-gdzie §2 #3 | AI NIE · HC |
| Auto-podpięcie FV | Nigdy auto-link do `shipment` | Progi M-03 sortują recenzję | §13m; F10 | ai-gdzie §2 #4 | AI NIE |
| Score dopasowania FV / suma linii **w modelu** | Drabina i suma = SQL; Decimal z akceptowanego draftu | Ranking SQL zostaje | Nie mylić z F10 „ranking SQL” jako zgodą na score LLM | ai-gdzie §2 #5 | AI NIE |
| Parser KSeF FA(3) przez LLM | XML + XSD, nie instructor | Parser deterministyczny | F9/F10 | ai-gdzie §2 #6 | AI NIE |
| Auto-zapis skanu gdy **jest** kod Omni / LLM zamiast skanera | Tor QR = SQL + `source_ref=scan://` bez LLM | HITL gdy **brak** kodu | D9 milczał że tor QR ≠ LLM | ai-gdzie §2 #7 | AI NIE |
| Auto-scoring osoby / JDG | Minimal risk tylko przy HITL i braku scoringu osoby | Fakty + wywiadownia + HITL | C#6; AI Act | ai-gdzie §2 #8 | AI NIE · prawo |
| GAN / inpainting glifów | Nowa treść na FV/CMR | Enhance = OpenCV + Lanczos | C#20; Zyrek 2025 | ai-gdzie §2 #9 | AI NIE |
| Accept bo pewność / optimistic UI | Pewność sortuje kolejkę, nie zastępuje kliknięcia | — | C#19; ADR-0003; ui-04 | ai-gdzie §2 #10 | AI NIE |
| RAG na wycenie / VAT / schemacie DB | RAG tylko SOP / ADR / maile / docs API | Knowledge Base w tabeli 2 | C#16; HC-08 | ai-gdzie §2 #11 | AI NIE · HC |
| OCR koperty / znaczek z LLM / scraping PP | Numer nadania / imię EPO z OCR koperty; koszt znaczka z LLM; śledzenie HTML | REST/EN + skaner HID; imię = EPO albo HITL ze skanu; znaczek = `charge` + `source_ref` | C#24 imię bez EPO; C#11 scraping | ai-gdzie §2 #12 | AI NIE |

#### Lista 3 — SZARE (ledger + Art. 50 + HITL; nie P0 nocy)

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| ETA / slot + ledger | Predykcja zmierzona; LLM nie liczy ETA | V1+V2 w tabeli 1 to funkcje fal, ten wiersz = job listy 3 | HITL zanim status klienta | ai-gdzie §3 #1 | AI SZARE · HZ |
| AI Summary / AI summaries (wątki mailowe) | Streszczenie po HITL; nie zapis encji | Label Art. 50 | Nie kolejka M-20. Odrzut z powodem albo HZ | ai-gdzie §3 #2; rozmowa #8; PDF §10 | AI SZARE · HZ |
| Chat → reguła walidacji (AI Validation Rules / AI Rule Builder) | Tekst → dane → test na próbie → człowiek włącza | Konfiguracja = dane (zasada 2) | LLM nie pisze reguł w kodzie. T5 = SQL, nie LLM | ai-gdzie §3 #3; rozmowa #9 | AI SZARE · HZ |
| Czat o rekordach / copilot wieży / AI chat agent (M-57) | Pytania o rekordy; szkice, nie czat-zapis. Alias PDF: AI chat agent | Art. 50 | PLAN S56/S58: nigdy auto-send | ai-gdzie §3 #4; PDF §10 | AI SZARE · HZ |
| Agent zakupowy (Carrier procurement agent) | RFQ→odpowiedzi→ranking; award HITL | Ranking = propozycja | Nie live HTTP z modelu. Nie mylić z Dispatch / Ocean Email AI | ai-gdzie §3 #5; matryca §10 | AI SZARE · HZ |
| Narracja CFO / raport po SQL (Generator raportów) | Zdania z pól SQL; LLM nie liczy | M-15, S57 | Rozszerzenia predykcyjne = F/V, nie noc | ai-gdzie §3 #6; PDF §12 | AI SZARE · HZ |
| Anomalia / fraud jako flaga (Fraud & Anomaly Engine) | Flaga do recenzji ≠ werdykt | M-54 | Nie scoring osoby (tabela 4) | ai-gdzie §3 #7 | AI SZARE · HZ |
| Ryzyko kontrahenta / early warning zarządu | Podmiot, nigdy osoba; Decision Ledger | Wieża V6 | Early Warning w tabeli 2 = słownik statusów, nie ten job | ai-gdzie §3 #8 | AI SZARE · V/HZ |
| Contract Intelligence | Diff FV vs umowa + HITL; kwoty Decimal po accept | — | Po żywym `purchase_invoice` | ai-gdzie §3 #9; PDF §12 | AI SZARE · HZ |
| Negocjacje w limitach (Autonomous Negotiation Engine) | Limity z danych + HITL; marża w `charge` | — | HZ ostrożnie; proza po §4 to nie wiersz tabeli 4 | ai-gdzie §3 #10 | AI SZARE · HZ |
| SQL z modelu przez `sqlglot` | Zapytania tylko przez `sqlglot`; nie logika wyceny | AGENTS | Nie silnik M-21 | ai-gdzie §3 #11 | AI SZARE |
| Digital twin / Omni Market forecasts | B0 = zdarzenia + Prediction Ledger zanim „AI przewiduje” | Twin od dnia 1 = B0+V1, nie 8 twinów PDF | Park / HZ; zakaz obietnicy magii. Pełne twiny = odroczone | ai-gdzie §3 #12; rozmowa #16 | AI SZARE · HZ |

---

## 1. Zaplanowane w 100%

Funkcja ma ID w [kolejka-propozycja.md](kolejka-propozycja.md) (albo M10/B0) **i** wiersz w matrycy. To **analiza**, nie kanon nocy. Pola: [pola-wizja-2026-09.md](pola-wizja-2026-09.md) + karty T1–T5 i T7 — Plan tnie do plastra. D8, F5, F7, C2, V7 są w sekcji 3 (TO_VERIFY jest ich rdzeniem). **Sklejki zostają** (47 wierszy); rozklejenie T6≠X8, V5≠V6, F9≠F10, X9≠X6 jest w Inwentarzu UI i w tabeli 5. Aliasy PDF (28) dopisane w kolumnie Funkcja albo Co robi.

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| M10-1 dedup | Jeden `party` na NIP/VAT-EU/EORI/DUNS; bez ID biznesowego = odmowa | Dedup w bazie; zakaz B2C egzekwowany (operator 2026-09-07) | Constraint bez M10-2 sklei oddział z matką | decyzja A#1; kolejka M10-1 | analiza · nie kanon |
| M10-2 role | Wiele ról na `party`; JDG = flaga; `parent_party_id` | Qargo: Company = customer i subcontractor | JDG → kredyt tylko HITL (AI Act / art. 22) | decyzja A#2; kolejka M10-2 | analiza · nie kanon |
| B0 ledger | `prediction_ledger`, `entity_event`, indeksy obok `nbp_rate`, `plan_snapshot`, TT z actuals | Bez logu z dnia 1 nie ma scorecardu predykcji | What-if = V8, nie B0. B0 bez T1 nie ma actuals TT. Digital twin „do wszystkiego” ≠ ten wiersz (tabela 5) | decyzja A#3; §13b | analiza · od startu |
| T1 `stop` (Stop Group / `stop_group`) | Punkt ZA/WY/cło/prom/terminal z oknem i statusem. Alias: Stop Group | Luka vs Qargo Order/Stop (9/10 twierdzeń API) | Nie mapa. `stop_group` jako osobny wiersz = tabela 5 T1b (Plan tnie grupę) | decyzja A#4; karta T1 | analiza · Fala T |
| T2 `trip`+`resource` ≈ Słownik naczep + dane osiowe | Jednostka wykonawczo-kosztowa: pojazd/kierowca/naczepa + podwykonawca z `party`. Alias PDF: Słownik naczep (Curtainsider, Mega, Reefer) + osie | ADR-0004: pierwsza proponowana fala po named parks; park S50 = brak jobu auto, nie „nigdy zasób” | Nie telematyka, nie tacho, nie własny HW. Kind naczepy rozklejony w tabeli 5 T2b | decyzja A#5; karta T2; pola-wizja §2 | analiza · Fala T |
| T3 `container` | Obiekt ISO 6346: plomby, PIN, D&D, VGM, reefer | SPEED/MC: kontener ≠ pole tekstowe na zleceniu | Nie booking armatorski (HZ). Nie na liście 32 tabel pól | decyzja A#6; karta T3 | analiza · Fala T |
| T4 podzlecenia | Zlecenie główne + relacje; rentowność = widok SQL na `charge` | SPEED: wynik spływa na główne | Zakaz drugiej tabeli marży (HC-03). Cost Allocation Engine ≠ ten widok (tabela 5) | decyzja A#7; karta T4 | analiza · Fala T |
| T5 task engine ≈ Workflow / custom workloads admina | Szablony zadań jako dane; warunki w SQL jak `applies_when`. Alias PDF: Workflow / custom workloads admina | Qargo Task na Order/Trip | Async dopiero z konsumentem outboxa (M-02 leftover). Nie LLM (AI Validation Rules = lista 3) | decyzja A#8; karta T5 | analiza · Fala T |
| T6 board + X8 podkłady ≈ Mapa planistyczna 1000 + polygon | Timeline/Blocks/Table/Legs; darmowe on/off u usera, płatne BYO u admina. Alias PDF: Mapa planistyczna 1000 + polygon (rozklejone: UI + tabela 5) | Puste km 31% UK / 25,9% UE (59 newsów + 44 case’y Qargo) | Mapa poza initial 250 kB. Zakaz `tile.openstreetmap.org`. T6 nie ma karty pól (tylko zapowiedź UI). **T6 ≠ X8** | decyzja A#9; §13k; kolejka T6/X8 | analiza · Fala T/X |
| T7 kurs wg daty | `fx_rate_basis` na opłacie (ETD / załadunek / D-1); SQL | Ustawa o VAT art. 31a; M-23 już jest | LLM/JS nie liczą. **Nie** auto-assign (kolizja ID T7 w matrycy §2 — tabela 5 T6e) | decyzja A#10; karta T7 | analiza · Fala T |
| D1–D3 drobnica ≈ Linehaul Schedule Engine; Dock time window; Dock scheduler | Linie+cutoff+TT; 4 poziomy + skan; cross-dock/awizacje. Aliasy PDF: Linehaul Schedule Engine; Dock time window; Dock scheduler | Siła SPEED (dossier 37 źródeł); iSPEED od XI 2025 | Nie pełny WMS (tabela 5). Nie optymalizator. Topologie hub&spoke = §13q (sekcja 2). Dock rozklejony D3b | decyzja A#11; kolejka D1–D3 | analiza · Fala D |
| D4 COD + POD/ROD | Pobrania i dokumenty zwrotne | Wzorzec SPEED; rozliczenie w Fali F | Nie giełda palet | kolejka D4 | analiza · Fala D |
| D5 cenniki drobnicowe | Strefy/waga/objętość/palety + FSC jako dane | Silnik wspólny z Falą P | Matching w SQL; nie T-SQL | kolejka D5 | analiza · Fala D |
| D6 LCL ≈ Consolidation Engine | Konsolidacje własne/obce + HBL/MBL + pule numerów. Alias PDF: Consolidation Engine | Wzorzec SPEED morze×drobnica | Nie booking armatorski | kolejka D6 | analiza · Fala D |
| D7 pallet pools | Saldo palet | Rozliczenie sald | Nie giełda palet | kolejka D7 | analiza · Fala D |
| D9 silnik wydruków ≈ Label Engine | Szablon = dane; 409 bez sieci; CMR/SSCC/ZPL; QR `shipment_ref`. Alias PDF: Label Engine | Qargo: brak etykiety = ładunek nie wejdzie na hub | Bez kodu Omni = HITL. M-38 dziś bez bajtów. Etykieta obcej sieci = D8 (sekcja 3). Groupage CMR i dwa tory QR = tabela 5 | decyzja A#12; §13n | analiza · Fala D |
| P0 leftover `charge.source_ref` | Nullable na starych fixture; obowiązkowe na INSERT z myta/PP | HC analog + V2b/F11 | **Brak kolumny dziś** (model 009). Nie nowa fala | kolejka P0 leftover; PROGRESS 2026-09-07 | leftover P0 · Fala P |
| P1–P4 rate card ≈ FSC per usługa | WHEN/IF/CALC/MIN/MAX; FSC; Local Charge + warning braków. Alias PDF: FSC per usługa (nie jeden globalny %). Charge templates = tabela 5 | ROHLIG SUUS ~rok poślizgu; Rhenus „łzy”; T-SQL odrzucony | Matching w SQL. Warning ≠ fakt. Marża w `charge`. P3b rozklejony | decyzja A#14; kolejka P1–P4 | analiza · Fala P |
| P5 expected vs actual ≈ Plan vs wykonanie; Trips to Bill | Snapshot kosztu tripa przy `in_transit` + wariancja. Aliasy PDF: Plan vs wykonanie (jakość planowania); Widok brakujących kosztów (Trips to Bill) | Qargo Knowledge Hub | Nie druga marża. AI Margin Guard (PDF) = sekcja 2, nie ten wiersz | decyzja A#15; kolejka P5 | analiza · Fala P |
| P6 tender quotes | Ważność i limit orderów z oferty | Pogłębienie M-25/26/29 | Tender Radar TED = sekcja 3. Tender AI / SIWZ = tabela 5 (inny job) | kolejka P6 | analiza · Fala P |
| X1–X2 portale | Klient: zlecenia/T&T. Przewoźnik: trip, POD, self-billing | Qargo: driver app + fakturowanie z FK najlepiej się sprzedaje | **Po Auth0 S53.** `/noc` pomija S53/S55. Named park ≠ ta fala. Dwie perspektywy Operator OS vs Enterprise = tabela 5 | decyzja A#16; kolejka X1–X2 | analiza · Fala X |
| X3 + X4 | Apka kierowcy = GPS L0 na czas zlecenia; pierwszy konsument outboxa | Konsument = warunek zdjęcia „nie Temporal na zapas” | Zgoda kierowcy. S59 OTel parked | decyzja A#17; kolejka X3–X4 | analiza · Fala X |
| X5 API publiczne | OAuth2 tenant/portal osobno | OpenAPI już wewnętrznie | Nie live bez Auth0 | kolejka X5 | analiza · Fala X |
| X7 lejek oferty ≈ Response Intelligence | `sent` / `pdf_viewed` / `replied` / `converted`; czasy w SQL; PDF z tokenem. Alias PDF: Response Intelligence (13j: ULEPSZ) | Mailto bez Graph: załącznik nie da sygnału — link PDF da | Piksel tylko po zgodzie. `email_opened` niska pewność (Apple MPP). `delivered`/`lost` = UI warstw. Podstawa prawna klika = sekcja 3 | decyzja A#18; §13i | analiza · Fala X |
| X9 + X6 skan ≈ Import zleceń obcych spedycji | Gate + OpenCV (~300 DPI Lanczos) + bbox + split HITL; diff CMR. Alias PDF: Import zleceń obcych spedycji | Qargo Document Intelligence; Photo POD „zrób ponownie” | Nie GAN. Kwota z `amount_text` przy accept. Optimistic accept zakazany. M-20 dziś split bez bbox. **X9 ≠ X6** (tabela 5) | decyzja A#19; §13o; §10 | analiza · Fala X |
| F1 KSeF live | FA(3), tryby, QR — Omni wystawia | Mandat PL w mocy 2026 | Dziś S35 = numer sesji, nie live HTTP. Nie KSeF z ERP | decyzja A#20; kolejka F1 | analiza · Fala F |
| F2 skonto / rezerwy | Skonto, rezerwy, rozliczenia wewnętrzne | Wzorce SPEED | Nie druga marża | kolejka F2 | analiza · Fala F |
| F3 noty + closing ≈ Financial controlling | Noty księgowe, zamknięcie okresu. Alias PDF: Financial controlling | Wzorzec SPEED | JPK zostaje w ERP (rejestr) | kolejka F3 | analiza · Fala F |
| F4 bank ISO 20022 ≈ Bank Adapter Layer | CAMT/MT940 + rekoncyliacja HITL. Alias PDF: Bank Adapter Layer | Pogłębienie M-42 | Bramka białej listy przed przelewem = §13q (sekcja 2). Nie auto-płatność | kolejka F4 | analiza · Fala F |
| F6 windykacja ≈ Credit warning przy limicie | Limity kredytowe w akcji; blokada zlecenia. Alias PDF: Credit warning przy limicie | Pogłębienie M-14/M-24 | Nie auto-scoring JDG | kolejka F6 | analiza · Fala F |
| F8 Peppol | Kanał e-faktur UE | Kalendarz UE | Nie zastępuje KSeF PL | kolejka F8 | analiza · Fala F |
| F9 + F10 ERP + FV kosztowa | Adapter FS+FZ; ingest mail/KSeF/skan → ranking SQL → HITL. **F9 ≠ F10** (tabela 5) | Operator 2026-09-07: Omni wystawia, ERP nie liczy marży | Agent outbound. Nigdy auto-link. XML FA(3) bez LLM. Licencje ERP = sekcja 3. Drabina 6 szczebli = tabela 5 | decyzja A#21; §13l–m | analiza · Fala F |
| F11 książka nadawcza | `paper_post` → `postal_dispatch` + EN + EPO | Dwa oficjalne API PP; max 500 w kopercie EN | Papier ≠ wyłączenie KSeF. Imię tylko EPO. USB/HID i znaczek na `charge` = tabela 5. Umowa EN/EPO = sekcja 3 | decyzja A#22; §13p | analiza · Fala F |
| C1+C7+C8 | SENT+GEO; katalog `monitoring_scheme`; `party_document` blokuje `POST shipment` | P0: SENT, EKAER, RO e-Transport, BDO, DIWASS gdy API. WSR od 21.05.2026 | Brak klona SENT w SK/CZ/AT/…. Nie scoring osoby. GR/BG = sekcja 3. `relation_document_requirement` i `shipment_monitoring_filing` = inwentarz 32 | decyzja A#23; §13h | analiza · Fala C |
| C3 lookup | Biała lista / VIES / GUS live | Pogłębienie M-10 lookup | To nie bramka płatności (§13q) | kolejka C3 | analiza · Fala C |
| C4 eCMR / eFTI | Elektroniczny list + eFTI | Cel 2027; interop DIWASS | Nie Selenium na portalach | kolejka C4 | analiza · Fala C |
| C5 CO₂ ≈ Carbon Data Layer ≠ raport ESG | GLEC/GHG; metodologia+wersja+źródło. Alias PDF: Carbon Data Layer ≠ raport ESG | Nie jedna „uniwersalna” liczba | IMO DCS/CII i ETS = sekcja 3 | kolejka C5 | analiza · Fala C |
| C6 odpady | BDO/KPO kraj + DIWASS/WSR transgranica | Oficjalne API MOS + KE | Zmiana BDO API **1.01.2027**. DIWASS dostęp = sekcja 3 | kolejka C6; §13h | analiza · Fala C |
| C9 snapshot Trans.eu | `overall_rating`, satisfaction, TransRisk, `documents.expire_date` | Oficjalne partners-api potwierdzone IX 2026 | Opinie słowne: **brak** publicznego endpointu — sekcja 3. Nie scrapować. Tabela: `party_exchange_snapshot` | decyzja A#24; §13h; kolejka C9 | analiza · Fala C |
| V1 Prediction Ledger ≈ Karty naukowe; Champion/challenger + drift detection | Rekord predykcji + scorecard. Aliasy PDF: Karty naukowe (model/data/prediction card); Champion/challenger + drift detection | Fundament wiarygodności vs „AI przewiduje” | ETA bez MAE/CRPS = zakaz | kolejka V1; §10 | analiza · Fala V |
| V2 ETA + pogoda ≈ Traffic live + historyczny | Planned/historical/live/risk-adjusted; Open-Meteo **wzdłuż trasy w całej Europie**. Alias PDF: Traffic live + historyczny (warstwy ETA; feed korków HERE/TomTom = tabela 5 V2c) | project44: +28 pp @ 10 h ±2 h (500+ FTL). Evmides 2024 MAE 99,9 min (AIS, nie LLM) | Free Open-Meteo **nie** do SaaS (Terms). Produkcja: płatny plan albo self-host AGPL. Dwa ETA fizyczne vs prawne = tabela 5 | kolejka V2; §13h; dostępy | analiza · Fala V |
| V2b myto EU/EFTA | Klasa/osie/emisja/CO₂/data; winieta osobno; `charge` z `source_ref` | Nie ma jednego darmowego API UE — plan to mówi wprost | Brak taryfy = warning, nie zmyślona kwota. Wybór silnika = sekcja 3. Ograniczenia masa/oś odcinka ≠ taryfa myta (tabela 5) | kolejka V2b; §13h | analiza · Fala V |
| V3 D&D + rollover | Watchdog D&D; detekcja rollover ETD/ETA | Morze; SPEED/MC | Blank sailing / congestion / readiness = §13q (sekcja 2), nie ten wiersz. Ferry watchdog = tabela 5 | kolejka V3 | analiza · Fala V |
| V4 AIS wieży | Lazy chunk AIS na wieży | Leftover S32 UI zamknięty 94.0+124.0 | **Leftover kanonu, nie V5.** `/noc` tego nie buduje jako Fala V | kolejka V4; CURRENT | leftover kanonu |
| V5 hub + V6 wieża ≈ Unified Telemetry Model; Data Normalization Engine (MC §95B) | `PositionEvent`; L0/L1a (`omni_telematic` = flota w umowie)/P0 PL (GBOX, IKOL, Flotis, Wialon)/L1b/L1c; external = 3 dni robocze bez trip, nowy trip włącza. Wieża: stock→EBITDA. **V5 ≠ V6** | Qargo bez wieży załadowcy. SPEED bez predykcji. Art. 5: minimalizacja na external | **Nie noc.** Zero własnego HW. AIS ≠ V5 | decyzja A#25; 2026-09-08 | analiza · Fala V |
| V5b giełdy tracking | Trans.eu monitoring/trace, TIMOCOM Tracking, Transporeon Open Visibility; `exchange_message` gdy tenant jest stroną | Oficjalne endpointy Trans.eu monitoring (docs) | Umowa live = sekcja 3. Teleroute = oferty, **nie** GPS. Zakaz scrapingu czatów | kolejka V5b; §13g | analiza · Fala V |
| V8 what-if ≈ Kontrfaktyczne przeplanowanie linii | Silnik scenariuszy na danych B0. Alias PDF: Kontrfaktyczne przeplanowanie linii | Wymaganie operatora + MC | Po V6. Nie B0. Linie NO/DE/SE + traffic = tabela 5 V8b | kolejka V8 | analiza · Fala V |

**Wierszy w tej tabeli: 47.**

---

## 2. Niezaplanowane z rozmowy i PDF

Rozmowa: **0 BRAK w matrycy** — nic z listy operatora nie milczy w matrycy. **75 BRAK w kolumnie Funkcja** tabel 1–4 — patrz Inwentarz + tabela 5. PDF: **42 nie wiszą poza planem**; ta tabela to **24 nazwy z §13q**, które nie mają ID fali T–V w kolejce (HZ albo ULEPSZ istniejącej fali), plus **1** luka kart pól z rozmowy (CZĘŚĆ). Dwanaście wierszy §13q z TO_VERIFY w rdzeniu jest w sekcji 3, żeby nie dublować. Dziesięć odrzuceń PDF — sekcja 4.

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| AI Margin Guard | Warning: trip stratny, FSC poniżej rynku, oferta powyżej mediany; sugerowana cena | Strażnik na `charge`, nie nowa marża | LLM **nie** liczy. Nie mylić z P5 | §13q; PDF s.23–24 | §13q · HZ (P/V) |
| Operational Service Agent | Ticket: klasyfikacja → root cause → propozycja (np. przesuń slot) → HITL | Inny job niż Customer Chat / IT Support Agent | Nie auto-zapis | §13q; PDF s.140–141 | §13q · HZ |
| Blank sailing prediction | Predykcja odwołanego rejsu | V3 dziś = D&D+rollover, nie blank sailing | Wpis do V1 ledger; nie LLM | §13q | §13q · V/HZ |
| Dispatch Agent | Alias dyspozytora T6+V7 | HITL | Nie osobny produkt | §13q; PDF s.354 | §13q · HZ |
| Biała lista jako bramka płatności | NIP+rachunek przed przelewem, weryfikacja masowa | C3 = lookup; F4 = CAMT — brakowało bramy „nie płać” | Nie drugi katalog kontrahenta | §13q; PDF s.256–257 | §13q · F (F4/C3) |
| Sankcje: UBO + bank + HS/CN + port | Poszerzenie zakresu M-53 | Nie nowy silos | UBO/bank nie były nazwane w wierszu M-53 | §13q; PDF s.183–184 | §13q · C/V |
| Knowledge Base | Trzecia warstwa chatu: Agent / Support / KB | HC-08: RAG wolno na SOP/docs | Nie stawki, nie VAT, nie schemat DB. Customer Chat = tabela 5 | §13q; PDF s.9–10 | §13q · X/HZ |
| Nakładki Parking/Fuel/Border/Ferries/Customs/Weather ≈ LEZ / green zones | Katalog on/off obok ruchu/LEZ/ORM. Alias PDF: LEZ / green zones jako silnik danych | §13k miał ruch, LEZ, OpenRailwayMap | Źródło per warstwa — część w sekcji 3. Satellite/Truck Restrictions = UI warstw | §13q; PDF s.20; §13k | §13q · V |
| Topologie sieci drobnicowej | Hub&spoke, milk-run, wiele magazynów/krajów jako dane | D1 = linie+cutoff, „nie optymalizator”; inwentarz fałszywie dawał MAT | Network Design Optimizer (OR) = niżej, nie ten wiersz | §13q; MC §23 | §13q · D1/V |
| Container Readiness Engine | Gotowość kontenera po konektorze | T3 = obiekt; Slot Intelligence ≠ readiness | Po API terminala | §13q; PDF s.285 | §13q · V/HZ |
| Port Congestion Prediction | Predykcja zatłoczenia portu | Wiersz V1 ledger | Nie LLM | §13q; PDF s.285 | §13q · V/HZ |
| Port Marketplace | Katalog Port→Terminal→Depot→Empty→Customs + fees | Dane, nie giełda slotów | Nie obietnica slotu (sekcja 4) | §13q; PDF s.293 | §13q · HZ |
| Terminal Appointment & Gate OS | Awizacja / brama + reschedule | SDK konektora ≠ orkiestracja bramy | Bez gwarancji „zawsze zarezerwujemy” | §13q; PDF s.291–310 | §13q · HZ |
| Data licensing layer | Per dataset: source, license, geography, frequency, ToS | `source_ref` ≠ licencja/geografia | Osobna tabela licencji | §13q; PDF s.368 | §13q · HZ ops/C |
| Omni Graph | `ContainerETAChanged` → slot, truck ETA, D&D, revenue risk | Szyna `entity_event` (B0) | Nie mylić z Business Impact Graph SKU→EBITDA (tabela 5) | §13q; PDF s.366–367 | §13q · V |
| Network Design Optimizer | Lokalizacja hubów / struktura linii | Silnik OR, nie LLM | ≠ VRP na istniejącej sieci. Multi-Objective Optimizer = tabela 5 | §13q; MC §95E | §13q · HZ |
| Demand Engine | Popyt na lane | Track record PDF „Demand 87,4%” — vendor, nie RCT | Wiersz rodzaju predykcji V1 | §13q; PDF s.172–176 | §13q · HZ |
| OMNI Market & Network Orchestrator | Giełdy+sieci+flota+magazyn+finansowanie jako zdolność | Parasol Make or Buy+D8 | Nie moduł „giełda”. HITL. Make or Buy jako wiersz = tabela 5 | §13q; PDF s.130 | §13q · HZ |
| Macro & Geopolitical Intelligence ≈ Prognozy cen frachtów/paliwa | Warstwa sygnałów (energia, polityka, żegluga). Alias PDF: Prognozy cen frachtów/paliwa | Korelacja ≠ przyczynowość zostaje | Nie „AI przewiduje wojnę” | §13q; PDF s.165–172 | §13q · V/HZ |
| Ocean Email AI | RFQ klienta → RFQ armatora → mail → parse → HITL | Inna powierzchnia niż Email Digital Twin + P4 | HITL; MaritimEmails F1 do 0,86 na **syntetyku**. Email Intelligence (klient→RFQ) = lista 1 | §13q; PDF s.332–333; ai-nauka | §13q · X/P |
| Logistics Autopilot | Dojrzałość 0–8 (pokazuje→…→wykonuje w granicach) | Reguła `/plan-modul` / DoD automatyzacji | Nie osobny produkt | §13q; PDF s.252, 358 | §13q · ops |
| Lineage ≈ Audit Engine (MC §95K) | Data + model + decision lineage. Alias PDF/MC: Audit Engine (MC §95K) | Decision Ledger i model card to wycinki | Ops/V1. Decision Ledger jako silnik §12 = tabela 5 | §13q; PDF s.367–368 | §13q · V1/ops |
| Early Warning GREEN/AMBER/RED/BLACK | Słownik statusów wieży | V6 bez nazwy/BLACK | Nie scoring osoby. Executive AI ≠ ten wiersz | §13q; PDF s.212–213 | §13q · V6 |
| e-Doręczenia | Skrzynka do urzędów ≠ książka PP | 13p miało tylko zdanie HZ | Nie F11 | §13q | §13q · HZ |
| Karty pól fal D/P/X/F/C/V | Kolumny do wpisania i zapisu poza Falą T | Operator żądał kart „teraz”; plan odkłada do `/plan-modul` (ADR-0004) | `karty-pol-fala-t.md` = tylko T1–T5 i T7. Nazwy pól wieczornych są w §13g–p, nie w pliku kart. To CZĘŚĆ z rozmowy, nie BRAK | audyt-rozmowa-vs-plan.md | luka kompletności |

**Wierszy w tej tabeli: 25.**

---

## 3. Wymaga weryfikacji

Brak API, umowy albo podstawy prawnej = **park**, nie teatr HTTP. Statusy ADR-0004: CONFIRMED / TO_VERIFY / PROPOSAL. Pierwsze 25 = [decyzja-operatora-wizja.md](decyzja-operatora-wizja.md) § B. Kolejne 12 = wiersze §13q, których rdzeń to TO_VERIFY i nie są już w § B pod tą nazwą.

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Auth0 / tenant (S53) | IdP produkcyjny przed portalami | PLAN: I1/I2 nie teraz; hello JWT zostaje | Bez tego X1/X2 i S55 = atrapa logowania. **Named park kanonu** | decyzja B#1; CURRENT | TO_VERIFY · named park |
| S21 kanały armatorskie | Live HTTP booking/tracking | Park w kanonie z powodem: brak umowy | Live bez kontraktu = teatr | decyzja B#2 | TO_VERIFY · named park |
| D8 etykiety sieci | Etykieta po **oficjalnym** API (Raben/Schenker/Hellmann/Palletforce/Alliance) | Qargo sam odsyła do systemu sieci | Udawany generator — odrzucone na stałe (sekcja 4) | decyzja B#3; kolejka D8 | TO_VERIFY API |
| V5b umowy tracking | Credentials Trans.eu monitoring/trace; TIMOCOM; Transporeon Open Visibility | Funkcja jest w sekcji 1 | Poll cudzej floty bez prawa. Teleroute ≠ GPS | decyzja B#4 | TO_VERIFY umowa |
| Czat giełd (własny tenant) | Historia messengera gdy tenant jest stroną | Wolno po oficjalnym API/eksporcie | Trans.eu: braku API historii (IX 2026). Kod bez API = scraping | decyzja B#5 | TO_VERIFY API |
| Opinie słowne Trans.eu | Lista komentarzy na profilu | Scoring z partners-api **jest** (C9) | Publicznego endpointu komentarzy nie ma; pytać `api@trans.eu`. Scraping odrzucony | decyzja B#6; audyt C9 vs §13h | TO_VERIFY · mail |
| L1c aggregator | Linkway INTEGRATOR / DRIP | Deklaracja vendorów ~230 / ~400 platform | Hub bez kontraktu = obietnica | decyzja B#7; dostępy | TO_VERIFY umowa |
| L1a Teltonika/Queclink | Codec / Air Interface **per model** | Wiki Teltonika publiczne; pakiet Omni (nie produkcja) | Adapter zgadujący ramkę. Queclink PDF nie jest swaggerem | decyzja B#8; §13g | TO_VERIFY per SKU |
| Native GPS poza P0 | Tronik ATRAX4, Logisat, reszta PL/EU | P0 w V5: GBOX, IKOL, Flotis, Wialon (IKOL/Flotis/Wialon: docs publiczne) | GBOX: docs.gbox.pl za loginem. Tronik/Logisat: swagger niepubliczny — **CZĘŚĆ** z rozmowy | decyzja B#9; audyt 5 CZĘŚĆ; dostępy | TO_VERIFY docs/umowa |
| Berg Insight / Geotab | Kolejność adapterów EU | Geotab po zakupie Verizon Connect EU (2025, poza ES) | Zła kolejność ≠ błąd prawny | decyzja B#10 | TO_VERIFY ranking |
| PUESC C2 | AIS-IMPORT / AES / Intrastat | Kolejka C2 | Formularz „celny” bez urzędu | decyzja B#11 | TO_VERIFY konto |
| Katalog SENT-europa | GR ICSISnet; BG e-Transport ustawa+API | C7 tylko potwierdzone systemy | Fałszywa zgodność = sekcja 4 | decyzja B#12 | TO_VERIFY źródło prawne |
| BDO API 1.01.2027 | Nowa spec MOS | Dziś swagger test-bdo.mos.gov.pl | Adapter pod stary kontrakt padnie w dniu zmiany | decyzja B#13 | TO_VERIFY spec |
| DIWASS | API KE dla oprogramowania komercyjnego (IR 2025/1290) | WSR od 21.05.2026 | Flaga odpadu bez zgłoszenia transgranicy. WSDL po Helpdesku | decyzja B#14; dostępy | TO_VERIFY dostęp |
| Myto EU/EFTA — wybór silnika | PTV / NAPSPAN / TollCalc vs taryfy publiczne | TollCalc ~37 krajów (deklaracja) | Strona TollCalc `/en/api.html` prawie pusta w fetch 2026-09-07. Brak taryfy = warning | decyzja B#15; dostępy | TO_VERIFY silnik |
| Nakordoni / Carto / Esri tiles | Licencja i atrybucja kafelków | Darmowe P0 = OpenFreeMap / GUGiK | TOS jak OSMF na `tile.openstreetmap.org`. **Nie** Nakordoni Truck Bans (zakazy jazdy = tabela 5) | decyzja B#16; §13k | TO_VERIFY licencja |
| X7 klik PDF — podstawa prawna | Hostowany PDF z tokenem | Link jest sygnałem; piksel tylko po zgodzie | Prawnik: umowa vs U.I. vs zgoda (EDPB 2/2023, CNIL 2026, PKE) | decyzja B#17; §13i | TO_VERIFY prawo |
| `delivered` maila | DSN / Graph delivery | Metryka lejka | Per skrzynka często brak | decyzja B#18 | TO_VERIFY per mailbox |
| EN + EPO (F11) | Umowa biznesowa PP + usługa EPO na przesyłce | Spec EN SOAP w96 + REST publiczne | REST śledzenia **nie** zwraca imienia. Obietnica „kto” bez EPO = sekcja 4. REST USS = inwentarz P0 | decyzja B#19; §13p | TO_VERIFY umowa |
| ERP P0 licencje | Comarch CDN/partner; Sfera nexo≠GT; Symfonia klucz aplikacji | Docs Symfonia publiczne | Surowy SQL do MSSQL = sekcja 4. Pięć adapterów nazwanych w inwentarzu P0 | decyzja B#20; erp-fk-adapter.md | TO_VERIFY licencja |
| F5 diety / F7 faktoring ≈ Remuneration engine | Stawki per kraj; partner faktoringu. Alias PDF: Remuneration engine (F5 szersze w 13e). **F5 ≠ F7** (tabela 5) | Kolejka F5/F7 | Kwoty diet z LLM / workflow bez wypłaty | decyzja B#21 | TO_VERIFY stawki/partner |
| V7 tacho / posting / art. 9 | Czas pracy, delegowanie, promy | Kolejka V7 | Prawo per kraj; apka **nie** poprawia tachografu. Driver Time Solver / Tacho Office = tabela 5 | decyzja B#22 | TO_VERIFY prawo |
| HZ konektory ≈ P&O Freight API | Booking per carrier; Baltic Hub OAuth2; BCT/GCT; P&O od 1.06.2026. Alias PDF: P&O Freight API (nazwa) | Oficjalne API tam, gdzie jest | HTTP na zgadywanych URL | decyzja B#23 | TO_VERIFY per carrier |
| Chłodnie zdalne | Sterowanie per urządzenie | — | API per device; bez kontraktu = zakaz | decyzja B#24 | TO_VERIFY API |
| Scanbot / cloud DI | Płatny SDK / cloud BYO | OpenCV+ML Kit/VisionKit = P0 bez tej licencji | Płatny skaner jako ukryty wymóg | decyzja B#25; §13o | TO_VERIFY licencja |
| Device Management BYO | IMEI, heartbeat, SIM tenanta — **portal producenta**, nie nasz firmware | Własny FOTA odrzucony (sekcja 4) | TO_VERIFY dostęp do portalu Teltonika/Queclink | §13q | TO_VERIFY · HZ |
| Tender Radar | TED Search + eForms | §13f = SIWZ klienta, nie feed TED | TO_VERIFY dostęp/licencja TED. Tender management / Tender AI = tabela 5 | §13q; PDF s.169 | TO_VERIFY TED |
| IMO DCS / CII | Zużycie paliwa statków ≥5000 GT | C5 = GLEC, nie IMO | TO_VERIFY kto składa (armator vs spedytor) | §13q; PDF s.159–160 | TO_VERIFY obowiązek |
| EU ETS + FuelEU Maritime | Compliance morski | ETS jako składnik ceny promu ≠ silnik | TO_VERIFY obowiązek tenanta | §13q; PDF s.159–160 | TO_VERIFY obowiązek |
| Cabotage Engine + RTPD | Licznik kabotażu; powrót kierowcy i pojazdu (2020/1057) | V7 = tacho/prom art. 9, nie kabotaż | TO_VERIFY prawo per kraj | §13q; PDF s.108–109 | TO_VERIFY prawo |
| Combined Transport | Reżim prawny (nie nogi Huckepack) | Intermodal ≠ combined. Huckepack = tabela 5 | TO_VERIFY | §13q; PDF s.108 | TO_VERIFY prawo |
| ZSL / SENT-GEO / e-TOLL L2 | Omni jako brama GPS → PUESC / e-TOLL | C1 = zgłoszenie SENT; 13h = taryfa e-TOLL jako myto | TO_VERIFY kto może być ZSL | §13q; PDF s.257–259 | TO_VERIFY uprawnienie |
| Fuel Price Intelligence | Stacja teraz vs następna (€, km) | 13j = anomalia paliwa, nie POI stacji | TO_VERIFY źródło cen stacji. Fuel fraud = tabela 5 | §13q; PDF s.204–206 | TO_VERIFY źródło |
| BYO kamera tenanta | Stream/incydent (np. Webfleet video) | Własny Video AI odrzucony | Prawo pracy / AI Act. **Nie** scoring osoby (sekcja 4) | §13q | TO_VERIFY prawo |
| Border Crossing Intelligence | Warstwa ETA „BORDER” + nakładka | V2 + §13k | TO_VERIFY źródło czasów odprawy | §13q; PDF s.20 | TO_VERIFY API |
| FerryGateway | Standard one-to-many operatorów promów | HZ „promy API” bez nazwy standardu | TO_VERIFY dostęp; B#23 pokrywa umowę, tu nazwa protokołu | §13q; PDF s.67–68 | TO_VERIFY dostęp |
| TachoSync / zdalny DDD | Konektor tam, gdzie urządzenie umie | V7 ogólnie ≠ nazwa TachoSync | TO_VERIFY per model | §13q; PDF s.83–86 | TO_VERIFY per model |

**Wierszy w tej tabeli: 37.**

---

## 4. Odrzucamy

Odrzucone na stałe ≠ odroczone do HZ. Drugie może wrócić po decyzji; pierwsze nie wchodzi do kodu. Najpierw **10 z PDF** (rejestr po §13q), potem **25 z decyzji operatora § C**. WMS pełny i AIR OS nie są tu — są w tabeli 5 jako granica / HZ (nie przeniesione do „zaplanowane”).

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Driver Score **bez człowieka** | Safety/Fuel/Smoothness zapisane jako ocena | KPI + szkic po DPA = M14b / V | AI Act + art. 22 | rejestr; 2026-09-08 | **auto-zapis na stałe**; sugestia+S11 = kanon |
| Driver Profitability **bez człowieka** | Revenue/fuel/accident jako ocena osoby | Koszt tripa na `charge` | art. 22 | rejestr; 2026-09-08 | **auto-zapis na stałe** |
| Własny Video AI / DMS / ADAS / OmniVision | Produkt kamer Omni | BYO kamera = HZ TO_VERIFY (sekcja 3) | Zero własnego HW wideo | rejestr; L-33 | na stałe (biznes) |
| FOTA / Device Management **własnego** firmware | IMEI/OTA naszego stosu | BYO portal producenta = §13q | Zero własnego HW; FOTA Omni nie powstaje | rejestr; L-02 vs L-33 | na stałe (biznes) |
| VAT OSS / IOSS | Rozliczenie B2C/B2B OSS | — | B2C poza produktem; B2B OSS nie jest jobem tenanta spedycyjnego | rejestr; L-34 | na stałe (biznes) |
| Benchmarki między tenantami | Market Intelligence z danych poufnych | Tylko dane licencjonowane / własne | HC-01 + MC §93 zasada 5 | rejestr; L-35 | na stałe |
| Selenium / automatyzacja logowania do portalu terminala | Bot na portal-only | Portal-fallback = zadanie człowiekowi | PDF s.309, 296: zakaz | rejestr; L-36 | na stałe |
| Gwarancja „zawsze zarezerwujemy slot” | Obietnica slotu | Gate OS = HZ po API | PDF s.290: capability matrix, brak API | rejestr; L-37 | odrzucone jako gwarancja |
| JPK jako moduł Omni | Silnik fiskalny w Omni | Prawda JPK w ERP/FK; adapter nie liczy | §13l | rejestr; L-40 | na stałe |
| Scoring osoby z wideo **bez człowieka** | Zmęczenie/telefon/ADAS jako ocena | BYO ingest + DPA + szkic HITL = kanon | AI Act + art. 22 | 2026-09-08 | **auto-zapis na stałe** |
| Rewrite Django / GraphQL / Apollo / Zustand / Ant | Zmiana stosu | — | Zero zysku domenowego; utrata 128 plastrów; ADR-0002 | decyzja C#1; ADR-0004 2026-09-07 | na stałe |
| Klon Qargo 1:1 | Road-first 1:1 | Qargo bez KSeF/SENT/białej listy, bez wieży załadowcy | — | decyzja C#2; ADR-0004 | na stałe |
| 200 modułów bez stop/trip/zasób | Katalog silosów zamiast warstwy wykonawczej | — | Zlecenie bez wykonania nie domyka jobu | decyzja C#3; ADR-0004 | na stałe (kolejność) |
| Cenniki/wydruki jako ręczne T-SQL | Mechanizm SPEED | Funkcja (rate card, szablon) = dane | Każde wdrożenie = dialekt | decyzja C#4; rejestr | mechanizm na stałe |
| Kod, branding, assety, teksty docs Qargo/SPEED | Kopiowanie IP | Odtwarzamy funkcjonalność i wzorce UX | Prawo autorskie | decyzja C#5 | na stałe |
| Auto-decyzja kredytowa JDG / osoby | Score/limit zapisany bez S11 | Fakty + raport + **szkic AI** + S11 = M14b | Art. 22 + AI Act | decyzja C#6; 2026-09-08 | **auto-decyzja na stałe**; sugestia = kanon |
| B2C / osoby prywatne bez NIP | Rekord bez ID biznesowego | M10-1 odmawia zapisu | Decyzja operatora 2026-09-07 | decyzja C#7 | na stałe (biznes) |
| BIK / systemy bankowe | Weryfikacja kredytowa bankowa | Zostają KRD, Coface, D&B, CreditSafe (tabela 5: lookup HITL) | Decyzja 2026-09-07 | decyzja C#8 | odrzucone (decyzja) |
| Własne urządzenia GPS | Projekt / produkcja / firmware Omni | HW = Teltonika+Queclink u przewoźnika, który chce pakiet | Decyzja 2026-09-07 | decyzja C#9; §13g | na stałe (biznes) |
| Poll floty na **zewnętrznym** GPS poza 3 dniami roboczymi | Continuous track bez zlecenia | `omni_telematic` + umowa = flota OK; external = 3 dni robocze, nowy trip włącza | Art. 5 | decyzja C#10; 2026-09-08 | **external poza oknem na stałe** |
| Scraping WCA / giełd / terminali / śledzenia PP / Envelo | Dane bez umowy | PP ma REST/EN | ToS + prawo + NIS2 | decyzja C#11 | na stałe |
| Podsłuch / scraping czatów giełd gdy tenant nie jest stroną | Stawki z cudzego messengera | Własne wiadomości tenanta po API | Art. 267 KK + RODO + ToS. Brak API historii (IX 2026) | decyzja C#12 | na stałe (prawo) |
| Wymyślanie narodowych „SENT-ów” | Adapter w kraju bez klona | Katalog tylko ze źródłem prawnym | Większość UE nie ma klona | decyzja C#13; §13h | na stałe |
| Scraping opinii słownych Trans.eu / TIMOCOM | Komentarze z profili | Scoring z partners-api jest oficjalny | Brak publicznego API komentarzy (IX 2026) | decyzja C#14 | na stałe |
| Niewidoczny piksel / tracker 3rd party / tracking osób prywatnych | Tracking bez zgody | Link PDF + zgoda na piksel = §13i | ePrivacy; EDPB 2/2023; PKE; CNIL 2026 | decyzja C#15 | na stałe (prawo) |
| RAG / pgvector na wycenie, VAT, schemacie DB | „AI zna stawki” | RAG wolno na SOP/docs (HC-08) | HC-08 | decyzja C#16 | na stałe (HC) |
| `tile.openstreetmap.org` jako CDN | Kafelki OSMF w produkcji | OpenFreeMap / GUGiK / self-host | Polityka OSMF: serwer społecznościowy ≠ CDN aplikacji | decyzja C#17; §13k | na stałe |
| HERE jako **baza** map/telematyki | Licencja asset-management jako podkład | Premium BYO OK | PDF s.66 | decyzja C#18 | odrzucone jako podstawa |
| Auto-zlecenie / auto-`charge` / auto-link FV / accept bo pewność | Straight-through z maila, geofence, skanu, extractu | Propozycja tak, zapis po człowieku | HC-04 + ADR-0003. DocILE residual ~30%; Goddard RR 1,26; Skitka commission | decyzja C#19; §10 | na stałe |
| Real-ESRGAN / GFPGAN / inpainting glifów | „Dopisz cyfrę” na FV/CMR | Enhance = OpenCV, DPI = Lanczos (CREASE) | Zyrek et al. 2025: GAN hallucinate glyphs | decyzja C#20; §13o | na stałe |
| Udawany generator etykiet Palletforce/Alliance | Fałszywa etykieta sieci | Import do systemu sieci gdy brak API | Qargo też odsyła | decyzja C#21; D8 | na stałe |
| Podwójny KSeF; ERP nadpisuje `charge` | Dwa wystawienia / druga marża | Wystawia wyłącznie Omni | Decyzja 2026-09-07; HC-03 | decyzja C#22 | na stałe |
| Surowy SQL / `sa` do Comarch/Subiekt/Symfonia | Bypass Sfery/CDN/WebAPI | Agent outbound | Psuje gwarancję i RLS po ich stronie | decyzja C#23 | na stałe |
| Gwarancja „kto odebrał” bez EPO | Imię z REST śledzenia | Imię = `getEPOStatus` albo HITL ze skanu | REST PP nie ma imienia | decyzja C#24; §13p | odrzucone jako gwarancja |
| Dwa produkty; 200 silosów; „AI przewiduje”; „100% zgodność prawna”; SLA 8 min / 4 h; Temporal na zapas | Copy mockupu jako DoD | Jeden core, dwie perspektywy (tabela 5). Skuteczność = Prediction Ledger. Outbox consumer najpierw (X4) | MC + ADR + rejestr | decyzja C#25 | na stałe / warunek |

**Wierszy w tej tabeli: 35.**

**Odroczone (HZ, nie „nie”)** — wiersze w tabeli 5, nie tylko proza: WhatsApp; Energy Intelligence; mikroserwisy; Connected Carrier / finansowanie GPS (HW własny i tak odrzucony); digital twins pełne / Omni Network Digital Twin; Disruption War Room; Autonomous Negotiation Engine tylko z limitami+HITL.

---

## 5. Nowe i rozklejone wiersze (rozmowa + PDF)

Jeden wiersz na koncept. Overlap rozmowa×PDF: oba źródła w kolumnie Źródło. Status z decyzji A/B/C gdy znany; **nie** pin do PLAN. Nazwy z [luki-rozmowa-vs-stan.md](luki-rozmowa-vs-stan.md) (75) i [luki-pdf-vs-stan.md](luki-pdf-vs-stan.md) (136) są albo tu, albo aliasem w tabelach 1–4, albo w Inwentarzu warstw.

### 5.1 Rozklejone sklejki (T6≠X8, V5≠V6, F9≠F10, X9≠X6, F5≠F7)

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| T6 planning board (≠ X8) | Timeline / Blocks / Table / Legs; gęstość A+/A−; zasób intermodal na boardzie (T6f) | Decyzja A#9 | Nie mapa. Karta pól T6 = świadoma luka | A#9; rozmowa #72 | analiza · Fala T |
| X8 mapa / `map_basemap` (≠ T6) | Katalog podkładów; seed darmowych; `is_blocked` osm.org; atrybucja | P0 OpenFreeMap + GUGiK | Instrukcja admina = X8b. Nie 1000 markerów (UI lazy map) | A#9; rozmowa #30 | analiza · Fala X |
| V5 hub `PositionEvent` (≠ V6) | Normalizacja GPS; L0/L1a/P0 PL/L1b/L1c; okno = `trip` + grace | Unified Telemetry / Data Normalization Engine = aliasy w tabeli 1 | Zero własnego HW. Nie wieża EBITDA | A#25; rozmowa #25 | analiza · Fala V |
| V6 wieża (≠ V5) | stock→produkcja→sprzedaż→EBITDA; „co jeśli”; ui-06 | Załadowca, nie tylko flota | Nie noc. TIME-TO-FIX jako metryka = osobny wiersz | A#25; kolejka V6 | analiza · Fala V |
| F9 Adapter FS+FZ (≠ F10) | Pięć konektorów P0 + `erp_connector` / `erp_series_map` / `erp_export`; agent outbound | Omni wystawia; ERP nie liczy marży | Licencje = B#20. Optima ≠ XL ≠ nexo ≠ GT ≠ Symfonia | A#21; rozmowa #43 | analiza · Fala F |
| F10 ingest FV kosztowej (≠ F9) | Mail/KSeF/skan → `purchase_invoice` po HITL; ranking SQL | Nigdy auto-link | XML FA(3) bez LLM. Drabina = F10b | A#21; §13m | analiza · Fala F |
| X9 skan/OpenCV (≠ X6) | Gate + enhance + bbox + split; Photo POD | Geometria przed LLM | Nie GAN. Nie diff vs zlecenie | A#19; §13o | analiza · Fala X |
| X6 diff CMR/POD (≠ X9) | Diff pól dokumentu vs zlecenie | Konflikty do recenzji | Nie capture/enhance | A#19; ai-gdzie #9 | analiza · Fala X |
| F5 diety / Remuneration engine (≠ F7) | Stawki diet per kraj; 13e szersze niż diety | Kolejka F5 | Kwoty z LLM = zakaz. TO_VERIFY stawki | B#21; PDF 13e | TO_VERIFY stawki |
| F7 faktoring / CFO (≠ F5) | Partner faktoringu; workflow wypłaty | Kolejka F7 | Workflow bez wypłaty = atrapa | B#21; rozmowa #71 | TO_VERIFY partner |

### 5.2 Planowanie, mapa, widoki, zasoby

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| T1b Stop Group | Grupowanie stopów (dostawy / groupage) | Matryca §2 `stop_group` | Plan tnie grupę; minus T1 to nie wiersz | rozmowa #12; matryca §2 | analiza · nie kanon |
| Consignment | Obiekt między order a stop (wzorzec Qargo) | D2 paczka ≠ consignment | Nie dublować `shipment_package` bez Planu | rozmowa #11 | analiza · nie kanon |
| T6e Auto-assign resources | Propozycja zasobu; człowiek zatwierdza | Matryca §2 T7 auto-assign | **Kolizja ID** z T7 kursu VAT — tu T6e, nie T7 | rozmowa #13; matryca §2 | analiza · nie kanon |
| Widoki per rola (drobnica ≠ FTL ≠ morze) | Trzy boardy, jeden model `stop`/`trip` | Spedytor A→B ≠ dyspozytor drobnicy | Nie trzy produkty (C#25) | rozmowa #15; PDF §12 | analiza · nie kanon |
| Markery stopów | Collection = trójkąt; Delivery = kwadrat; Other = koło; kolor = status | §13k ma podkłady, zero markerów | Lazy, nie initial bundle | rozmowa #4 | analiza · nie kanon |
| Saved views A+/A− | Widoki prywatne i zespołowe / org; gęstość na boardzie T6 | `table_view` w kodzie = siatki | Gęstość A+/A− na T6 nie jest w `table_view` | rozmowa #6; matryca §11 | analiza · część w kodzie |
| T2b kind naczepy + osie | Słownik naczep + `axle_count`; myto czyta to samo | Alias w T2 | Nie druga tabela myta | rozmowa #57; PDF 13j | analiza · nie kanon |
| Subcontractor bidding | Przetarg podwykonawcy + spread na `charge` | M-30/M-31 w kodzie | Nie live HTTP. `quoted_amount` osobno | rozmowa #14 | analiza · nie kanon |
| `quoted_amount` na `carrier_inquiry` | Cytowana cena z **naszego** kanału + waluta | Pola §3.6 | Nie cudzy podsłuch | rozmowa #27; V5b | analiza · nie kanon |
| Intermodal bulk move | Hurtowe przesunięcie zasobów intermodal na boardzie | T6f | Nie Combined Transport (sekcja 3) | PDF §5; rozmowa #72 | analiza · nie kanon |
| X8b instrukcja admina map | Skąd wziąć API podkładu; plik + UI | [podklady-map-admin.md](podklady-map-admin.md) | Nie nowy kod per vendor | rozmowa #29 | analiza · ops |
| Seed katalogu P0 map | OpenFreeMap, GUGiK, CyclOSM, HOT, Carto, … + `is_blocked` | Inwentarz P0 | Fair use Carto/Esri = TO_VERIFY | rozmowa #30; §13k | analiza · nie kanon |
| Operator OS vs Enterprise | Ten sam core, inny portal (X1 vs T6/V6) | C#25 odrzuca dwa produkty | Nie dwa SKU | rozmowa #65; §13j | analiza · nie kanon |
| Słowniki per tenant | Wartości enum jako dane tenanta | Zasada 2 | Nie twardy kod na zawsze | PDF §11 | analiza · nie kanon |
| Numeracja per lokalizacja / oddział | Prefiks numerów per oddział | M-03 szablony | Unikat `shipment_ref` per tenant zostaje | PDF §11 | analiza · nie kanon |
| Floating trailers | Naczepy bez stałego ciągnika | Katalog `resource` | Nie własny HW | PDF §13c | matryca · HZ |
| Multi-manning | Dwóch kierowców na trip | `driver_resource_id` dziś jeden | Plan tnie drugi slot | PDF §13c | matryca · HZ |
| Huckepack / wagony kieszeniowe | Noga kolejowa kieszeniowa | `shipment_leg` rail | Combined Transport = sekcja 3 (prawo) | PDF §13c | matryca · HZ |
| AIR OS / Air (lotnicze) | Moda lotnicza | `shipment_leg` dziś: road/rail/china_rail/ocean_lcl | Brak decyzji A. HZ albo świadomy POMIŃ | rozmowa #68; PDF §13c | matryca · HZ / POMIŃ |
| WMS pełny | Magazyn jako produkt | D1–D3: nie pełny WMS | Poza zakresem drobnicy. Nie tabela 4 (granica D, nie „na stałe” jak C#1) | rozmowa #69; PDF §13c | granica D · HZ |

### 5.3 HITL, skan, FV, poczta, `shipment_ref`

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| F10b drabina match FV | 6 szczebli SQL: `shipment_ref` → identifiers → NIP+kwota+data → wątek → lane → unassigned; progi 1-klik | `invoice_match_candidate` | Model nie scoruje. Nigdy auto-link | rozmowa #31; §13m | analiza · nie kanon |
| `shipment_ref` | Twardy numer na wydruku, QR, mailu, FV podwykonawcy | Obowiązkowy na wychodzących | Dziś brak kolumny (pola §2.1) | rozmowa #32; D9+F10 | analiza · nie kanon |
| F10c FV bez NIP (inne kontynenty) | Lista + `mail_draft` „podaj numer Omni”; brak zgadywania | HITL | Nie auto-party | rozmowa #33; §13m | analiza · nie kanon |
| F10d alokacja FZ | Jedna FZ → wiele zleceń; suma linii = kwota SQL. Alias: Dystrybucja: podział FV kosztowej do sztuki | `purchase_invoice_allocation` | Model nie sumuje | rozmowa #34; PDF §3 | analiza · nie kanon |
| F10e parser FA(3) | XSD parser KSeF zakup vs extract skanu | Deterministyczny | Lista 2 #6 | rozmowa #44; §13m | analiza · nie kanon |
| X9-capture ML Kit / VisionKit | Android `BASE_WITH_FILTER` / `FULL` nie na FV; iOS VisionKit | P0 bez licencji Scanbota | Scanbot zostaje B#25 TO_VERIFY | rozmowa #37; karta 010 | analiza · nie kanon |
| X9-enhance skaner płaski | Warp, deskew, biel, kolor vs B/W, Lanczos ~300; `scan_enhance_run` | Oryginał zostaje | Zakaz GAN = C#20 | rozmowa #38; §13o | analiza · nie kanon |
| Quality gate / „zrób zdjęcie ponownie” | Laplace, prostokąt; gate przed extractem | Photo POD | Nie LLM | rozmowa #39; §13o | analiza · nie kanon |
| D9b Groupage CMR | Osobny CMR na grupę dostaw / stop group | Wzorzec Qargo | Wymaga T1b | rozmowa #60; §13n | analiza · nie kanon |
| D9c dwa tory QR | Nasz QR `tenant+shipment+package+document_kind` = SQL od razu; bez kodu Omni = HITL | Karta 009 | Tor QR bez LLM (lista 2 #7) | rozmowa #73; §13n | analiza · nie kanon |
| F11a `paper_post` | `delivery_channel` na `party` i `sales_invoice`; papier → `postal_dispatch` | Papier ≠ wyłączenie KSeF | — | rozmowa #40; karta 011 | analiza · nie kanon |
| F11b `numer_nadania` USB/HID | Trzy ścieżki: skaner HID (klawiatura), zwrotka EN, wklejenie+checksum | HID = klawiatura, nie driver | Nie OCR koperty (lista 2 #12) | rozmowa #41; §13p | analiza · nie kanon |
| F11c znaczek PP na `charge` | Koszt znaczka = `charge` + `source_ref`, nie pole na książce | HC analog | Wymaga leftover P0 `source_ref` | rozmowa #74; §13p | analiza · leftover P0 |
| M-03 klucze HITL | `hitl_confidence_green` / `amber`, `invoice_match_suggest_min`, `telematics_grace_days` | Allowlista, nie sekrety | VARCHAR(64) | rozmowa #75; pola §1.2 | analiza · nie kanon |
| Charge templates | Szablony opłat jako dane | P1–P4 = silnik | Nie T-SQL | PDF §4 | analiza · nie kanon |
| P3b FSC per usługa | FSC jako dane per usługa, nie jeden globalny % | Alias w P1–P4 | Matching SQL | rozmowa #66; PDF 13j | analiza · nie kanon |

### 5.4 Telematyka, ETA, trasa, pogoda, zakazy

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| V5-P0 cztery adaptery | GBOX, IKOL, Flotis, Wialon jako własne joby native | IKOL/Flotis/Wialon: docs publiczne | GBOX docs za loginem (blokuje kompletny klient) | rozmowa #24; karta 006 | analiza · B#9 CZĘŚĆ |
| Diagnostyka spedytora | Za drogo vs brak aut vs kompetencja; metryki jobu na `entity_event` | Bez podsłuchu | Nie scoring osoby | rozmowa #26; §13g | analiza · nie kanon |
| V2-suplement IMGW / DWD / Météo-France | Narodowy feed obok Open-Meteo | Nie jedyne źródło | SaaS Open-Meteo i tak płatny/AGPL | rozmowa #28; karta 007 | analiza · nie kanon |
| Zakazy jazdy / `driving_ban_rule` | Święta/wakacje/upały; Nakordoni **Truck Bans** (nie kafelki B#16); Nager.Date; etransport.pl = kuracja, nie API | Matryca §13d | Nie mylić z licencją tiles | rozmowa #18; PDF §13d | analiza · nie kanon |
| NAPSPAN / DATEX II restrykcje | Wymiary, masa, nacisk na oś, tunele — dane odcinka + źródło | Overlay LEZ ≠ mass/axle | V2b osie = taryfa myta, nie zakaz odcinka | rozmowa #19; PDF §13d | analiza · nie kanon |
| V2c Traffic do TT | Źródło ruchu live + historyczny + TTL; HERE / TomTom / PTV jako feed (nie podkład) | Nie LLM | C#18: HERE nie jako **baza** map | rozmowa #20; PDF §13d | analiza · nie kanon |
| Dwa ETA: fizyczne vs prawne/operacyjne | Dwa czasy na trip/stop | V2 ma planned/historical/live/risk, nie ten split | — | rozmowa #47; PDF 13j | analiza · nie kanon |
| TIME-TO-FIX | SAFE/AMBER/RED + przyczyna | Wieża V6 | Nie scoring osoby | rozmowa #46; PDF 13j | analiza · nie kanon |
| `FERRY_REST_EVENT` + Ferry watchdog | Art. 9 odpoczynek na promu; ETA vs cut-off | V7 ogólnie ≠ ten event; V3 = D&D morze | Apka nie poprawia tacho | rozmowa #48; PDF 13j | analiza · nie kanon |
| Driver Time Solver | Warianty A–I jako dane | V7b | Apka nie „poprawia” tachografu | rozmowa #49; PDF 13j | analiza · nie kanon |
| Legal Feasibility Check + Compliance & Time Simulation | Wynik = ryzyko; symulacja minuta-po-minucie | Nie wyrok LLM | — | rozmowa #50; PDF 13j | analiza · nie kanon |
| Geofence → waiting charge | Propozycja waiting; HITL, nie auto-`charge` | — | C#19 | rozmowa #51; PDF 13j | analiza · nie kanon |
| Elektroniczna karta drogowa | Karta jako dokument/zdarzenia V7/F | — | Nie tacho firmware | rozmowa #52; PDF 13j | analiza · nie kanon |
| Fuel fraud / anomalia paliwa | Expected vs actual + GPS; flaga recenzji | Nie Fuel Price Intelligence (stacje) | Nie wyrok / nie scoring osoby | rozmowa #53; PDF 13j | analiza · nie kanon |
| Profil wysokości trasy | Osobno od pogody; `altitude_m` na `position_event` | — | Nie float-JSON | rozmowa #54; PDF 13j | analiza · nie kanon |
| Cache tras | TTL traffic / trasa / LEZ | — | Nie LLM | rozmowa #58; PDF 13j | analiza · nie kanon |
| Diagnostyka pojazdu / predictive maintenance | DTC / serwis jako flaga | `dtc_code` na PositionEvent | Nie scoring kierowcy | PDF §13c | matryca · HZ |
| Karty paliwowe + zbiorniki | Karty i stany zbiorników | — | Fuel fraud ≠ ten katalog | PDF §13c | matryca · HZ |
| Gospodarka oponami / serwis | Opony / warsztat | — | Nie OmniVision | PDF §13e | matryca · HZ |

### 5.5 Koszt, make-or-buy, VAT, bliźniak, C-level §12

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Cost Allocation Engine | Klucze DIRECT/SHARED/… jako dane | Marża zostaje w `charge` | T4 = widok SQL, nie ten silnik | rozmowa #45; PDF 13j | analiza · nie kanon |
| Make or Buy | Ten sam ładunek: własny tabor vs giełda vs sieć; koszt+ETA+FIX; HITL | Orchestrator = parasol | Nie auto-award | rozmowa #61; PDF 13j | analiza · nie kanon |
| Opportunity Engine | Oszczędność / ROI / owner | — | Nie scoring osoby | rozmowa #64; PDF 13j | §13q · HZ |
| VAT Engine | Traktowanie + stawka + podstawa; B2B; SQL; nie LLM | Katalog reguł | Nie VAT OSS (tabela 4) | rozmowa #55; PDF 13j | analiza · nie kanon |
| Terms AI | Ryzyko na obcym zleceniu + HITL | — | Nie auto-zapis warunków | rozmowa #56; PDF 13j | analiza · HITL |
| Akceptacja oferty z języka maila | „akceptujemy 1850 EUR” → szkic shipment HITL | M-29 CZĘŚĆ | HC-04 | rozmowa #59; PDF 13j | analiza · HITL |
| Cyfrowy bliźniak od dnia 1 | Twin = B0+V1 od startu; pełne 8 twinów PDF = HZ | Lista 3 #12 | Nie „na wszystko” w nocy. Omni Network Digital Twin = niżej | rozmowa #16; PDF §12 | analiza · B0; pełne = HZ |
| Twin what-if linie NO/DE/SE | Scenariusz linii drobnicowych + TT z actuals + zakazy + pogoda + traffic | V8b; Linehaul §13j | V8 ogólny ≠ ten scenariusz | rozmowa #17 | analiza · nie kanon |
| Omni Network Digital Twin | Twin sieci (pełny) | Odroczone „twiny pełne” | Nie B0 | PDF §12 | odroczone HZ |
| Business Impact Graph (SKU→EBITDA) | Graf SKU→EBITDA | Omni Graph ≠ ten graf | Wieża V6 to łańcuch, nie graf SKU | PDF §12 | matryca · HZ |
| Revenue at Risk + Working Capital Engine | Przychód zagrożony + kapitał obrotowy | — | LLM nie liczy | PDF §12 | matryca · HZ |
| Disruption War Room | Sala kryzysowa | Proza HZ po §4 | Nie Early Warning słownik | PDF §12 / §9 | odroczone HZ |
| Procurement Autopilot | Zakupy w granicach | Agent zakupowy = lista 3 | HITL award | PDF §12 | matryca · HZ |
| Regulatory Radar | Sygnały regulacji | — | Nie „100% zgodność” (C#25) | PDF §12 | matryca · HZ |
| Counterparty Risk Engine | Ryzyko kontrahenta (podmiot) | HITL | Nie JDG auto-score (C#6) | PDF §12 | matryca · HITL |
| Multi-Objective Optimizer | Wagi na istniejącej sieci | ≠ Network Design (lokalizacja hubów) | Nie LLM | PDF §12 | matryca · HZ |
| Memory Graph | Pamięć relacji / decyzji | Wzmianka przy Omni Graph | — | PDF §12 | matryca · HZ |
| Decision Ledger | Pełny rejestr decyzji | Lineage mówi „wycinek” | — | PDF §12 / §11 | matryca · HZ |
| Executive AI | Pytania zarządu | ≠ Early Warning | Art. 50; nie wyrok | PDF §12 | matryca · HZ |
| Energy Intelligence | Energia jako warstwa | Odroczone rejestr | — | PDF §12 | odroczone HZ |
| Customer Chat | Chatbot klienta: raporty i pytania | HITL; RAG tylko SOP | ≠ Knowledge Base; ≠ X1 portal. WhatsApp = odroczone | rozmowa #10; PDF §12 | §13q · HZ |
| IT Support Agent | Ticket IT | Wzmianka przy Operational Service Agent | Inny job | PDF §12 | §13q · HZ |
| Email Digital Twin | Twin wątku mailowego | ≠ Ocean Email AI; ≠ Email Intelligence | HITL | PDF §12 | matryca · HZ |
| Slot Intelligence + Secure Chain + Port Identity | Slot / łańcuch / tożsamość portu | Readiness ≠ Slot | Gwarancja slotu = tabela 4 | PDF §12 | matryca · HZ |
| Omni Market Intelligence | Produkt danych rynku | ≠ Macro geo; ≠ benchmarki tenantów (tabela 4) | Tylko dane licencjonowane | PDF §12 | matryca · HZ |
| Connected Carrier / telematyka jako biznes / 5 modeli | Model biznesowy GPS u przewoźnika | HW własny odrzucony (C#9) | Finansowanie GPS = odroczone | PDF §12 / §13j | odroczone HZ |
| Bliźniak urzędu | Proces/deadline urzędu; nie udawanie urzędu | — | Nie Selenium (tabela 4) | rozmowa #62; PDF 13j | matryca · HZ |
| Transformation Office | Biuro transformacji (ops) | — | Nie produkt TMS | PDF 13j | matryca · HZ |
| Spend leakage | Wyciek wydatków | SQL na `charge` | Nie druga marża | PDF 13j | matryca · HZ |
| Claims OS + Deadline Engine + słownik szkód | Reklamacje + deadline + katalog szkód | M-55 cargo_claim w kodzie | Nie kwota z LLM | PDF 13j / §13e | matryca · HZ |
| Network / resource costing | Koszt zasobu / sieci | — | Marża w `charge` | PDF §13e | matryca · HZ |
| Fleet cost model | Model kosztu floty | — | Nie Driver Profitability (tabela 4) | PDF §13e | matryca · HZ |
| Loading optimizer + VRP 1000+ | Załadunek + VRP | D1: nie optymalizator | Axle Load Optimizer = ten sam silnik (alias audytu B) | PDF §13e | matryca · HZ |
| Rentowność wielowymiarowa | Wymiary rentowności poza T4 | SQL na `charge` | Nie druga tabela marży | PDF §7 | matryca · HZ |
| Spot vs contract + historia rynkowa | Spot vs kontrakt + historia | Market data giełd osobno | Nie benchmarki tenantów | PDF §13c | matryca · HZ |
| Market data giełd (Transporeon Insights, accepted price) | Ceny przyjęte z giełdy licencjonowanej | — | Zakaz scrapingu | PDF §4 | matryca · TO_VERIFY licencja |
| Financial controlling | Controlling (alias F3) | Tabela 1 F3 | Nie JPK Omni | PDF §13c | alias F3 |

### 5.6 Przetargi, CRM, compliance, agenci, metrologia UX

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Tender Playbook / Playbook przetargowy / SIWZ | Analiza dokumentacji przetargowej (RFP/SIWZ); Playbook przetargowy; HITL | ≠ Tender Radar TED; ≠ P6 ważność oferty | Zakaz scrapingu kontaktów. Matryca = SQL+HITL, nie „bez błędów LLM” | rozmowa #21; PDF §13f | matryca · HZ |
| Tender management / Tender AI | SIWZ klienta jako proces | — | Nie TED | PDF §13c / §13f | matryca · HZ |
| Prospecting | Poszukiwanie przetargów / klientów | — | Nie scraping kontaktów | PDF §13f | matryca · HZ |
| Auto-wypełnianie matrycy przetargowej | Szkic komórek; HITL | — | Nie gwarancja bez błędów LLM | PDF §13f | matryca · HITL |
| Bid/no-bid | Decyzja startu | HITL | — | PDF §13f | matryca · HITL |
| Pomiar skuteczności przetargów | Metryki win/loss | SQL | — | PDF §13f | matryca · HZ |
| CRM | Relacje handlowe | Segmentacja A/B/C osobno | Nie drugi `party` | PDF §13c | matryca · HZ |
| Segmentacja handlowa A/B/C | ABC klientów | Dane, nie score osoby | — | PDF §13a | matryca · HZ |
| Wywiadownie (KRD / Coface / D&B / CreditSafe) | Lookup + HITL; analiza JDG tylko HITL | C#8 zostawia te źródła przy odrzucie BIK | Nie auto-score JDG (C#6) | rozmowa #23; PDF §13a | analiza · HITL |
| Contract management | Umowy jako obiekty | ≠ Contract Intelligence (diff FV) | HITL | PDF §13c | matryca · HZ |
| Compliance / Legal Engine | Silnik zgodności | Agenci ADR/Customs osobno | Nie wyrok LLM | PDF §13e | matryca · HZ |
| Agenci Transport / ADR / Customs / Legal Advisor | Agenci doradczy HITL | ADR advisor (matryca §8) osobno lub tu | Nie auto-klasa IMDG | PDF §13e | matryca · HZ |
| ADR advisor | Doradztwo ADR | M-52 katalog UN | LLM nie nadaje klasy | PDF §8 | matryca · HITL |
| Wirtualne biuro / Tacho Office | Biuro tacho / posting | V7 ogólnie ≠ nazwa | TO_VERIFY prawo = B#22 | PDF §13e | matryca · HZ |
| Ubezpieczenie cargo per zlecenie | Polisa na shipment | `party_document` OCP/OCS | Nie scoring | PDF §13e | matryca · HZ |
| Magazyn celny + miejsce uznane | Skład / miejsce uznane | — | PUESC C2 = sekcja 3 | PDF §13c | matryca · HZ |
| Incident management | Incydenty operacyjne | M-37 operational_exception w kodzie | — | PDF §13c | matryca · HZ |
| Fiscal risk scoring podmiotu | Score podmiotu (nie osoby) | HITL | Osoba/JDG = C#6 tabela 4 | PDF §13e | matryca · HITL podmiot |
| ISO 27001 / NIS2 | Wymogi ISMS / NIS2 | Ops | Nie produkt TMS | PDF §13e | ops · HZ |
| AI Agent Runtime (MC §95J) | Runtime agentów | Logistics Autopilot = dojrzałość 0–8 | Nie chatbot-kalkulator | PDF MC §95 | matryca · HZ |
| Copilot / Email AI / Document AI (warstwa) | AI CORE = extract HITL + agenci §13q | Lista 1 | Nie chatbot-kalkulator | rozmowa #70; Q §21 | analiza · HITL + HZ agenci |

### 5.7 Giełda, integracje, portale, SMS, sandbox, UX ops

| Funkcja | Co robi | Plus | Minus / ryzyko | Źródło | Status |
|---|---|---|---|---|---|
| Giełda zleceń dla przewoźników partnerskich | Oferty do partnerów | ≠ auto-wystawienie na giełdę publiczną | HITL | PDF §6 | matryca · HZ |
| Auto-wystawienie na giełdę | Publikacja frachtu | — | TO_VERIFY API; zakaz scrapingu | PDF §13e | matryca · TO_VERIFY |
| Webhooki outbound | Zdarzenia na URL tenanta | Idempotencja HC | Outbox = cel gdy zdarzenia między BC | PDF §6 | matryca · HZ |
| Bilety promowe w portalu | Bilet w X1/X2 | FerryGateway = sekcja 3 | — | PDF §6 | matryca · HZ |
| Integration Hub | Katalog konektorów: telematics / porty / prom / cło / ERP / WMS | Nie nowy silos | WMS pełny = granica D | rozmowa #67; PDF §13e | ops · katalog |
| SMS / e-mail outbound (bramki) | Bramki SMS/mail | `mail_draft` = szkic, nie Graph send | Auto-send zakazany | PDF §13e | matryca · HZ |
| Sandbox / demo per tenant | Środowisko demo | — | Nie dane produkcyjne | PDF §13e | ops · HZ |
| Import / migracja SID | Import ze SPEED/SID | — | Nie T-SQL cenników (C#4) | PDF §13e | matryca · HZ |
| Brama AI w module | AI tylko przy ROI + dowodzie; HITL extract tak; kalkulator/GAN/scoring nie | [ai-nauka-i-dowody.md](ai-nauka-i-dowody.md) | Ops, nie silnik | rozmowa #42 | ops · brama |
| Pomiar naukowy UX / A/B testy UI / SUS | Telemetria UI (PostHog w stosie) + protokół A/B testy UI; testy zadaniowe z pilotami (SUS); Pomiar czasu jobu operatora | Nie scoring osoby | — | rozmowa #22; PDF §13f | ops · metrologia |
| WhatsApp | Kanał klienta | Odroczone | Nie P0 nocy | proza po §4; §13q | odroczone HZ |

---

## Liczba wierszy

| Tabela | Wiersze |
|---|---|
| Zaplanowane w 100% | **47** (z aliasami; sklejki zachowane) |
| Niezaplanowane z rozmowy i PDF | **25** (z aliasami) |
| Wymaga weryfikacji | **37** (z aliasami) |
| Odrzucamy | **35** |
| **Suma tabel 1–4** | **144** |
| Inwentarz: 32 tabele | **32** |
| Inwentarz: powierzchnie UI | **8** |
| Inwentarz: P0 nazwane | **23** |
| Inwentarz: AI lista 1 / 2 / 3 | **12 + 12 + 12 = 36** |
| Tabela 5 (nowe + rozklejone) | **134** |

Tally pól **324/32** i dostępów **49** checkboxów **nie** oznacza, że tabele 1–4 pokrywają PDF 1:1.

---

## Jak sprawdzić

Operator może **Ctrl+F** nazwy z [luki-rozmowa-vs-stan.md](luki-rozmowa-vs-stan.md) (75 tematów, w tym dwadzieścia pierwszych: Select & Drop, Pre-planning, Mapa 1000 + polygon, Markery stopów, Satellite / Traffic / Truck Restrictions, Saved views A+/A−, Email Intelligence, AI Summary, AI Validation Rules, Chatbot klienta, Consignment, Stop Group, Auto-assign, Subcontractor bidding, Widok drobnica ≠ FTL, Cyfrowy bliźniak na wszystko, Twin what-if linie NO/DE/SE, Zakazy jazdy / etransport, Ograniczenia masa/oś/wymiary, Traffic do TT) oraz z [luki-pdf-vs-stan.md](luki-pdf-vs-stan.md) (136 nazw §2a–2h). Trafienie: własny wiersz **albo** jawny alias (`≈` / „Alias PDF”) w tabelach 1–4 **albo** Inwentarz warstw (tabela, UI, P0, job AI).

To nie jest obietnica „376 stron = 324 kolumny = 100% w planie”. To inwentarz, żeby nazwa nie ginęła w sklejce.

---

## Źródła (czytane, nie z pamięci)

- [luki-warstwy-vs-stan.md](luki-warstwy-vs-stan.md) — 23/32 tabel, UI, P0, AI 1/2/3
- [luki-rozmowa-vs-stan.md](luki-rozmowa-vs-stan.md) — 75 BRAK wierszy
- [luki-pdf-vs-stan.md](luki-pdf-vs-stan.md) — 136 nazw; 28 aliasów; 0 z ziarna 42 poza matrycą
- [audyt-rozmowa-vs-plan.md](audyt-rozmowa-vs-plan.md) — 18/5/0 **matryca**
- [audyt-pdf-chatgpt-luki.md](audyt-pdf-chatgpt-luki.md) — ziarno 42
- [benchmark-tms-2026.md](benchmark-tms-2026.md) §10, §13g–q, rejestr
- [kolejka-propozycja.md](kolejka-propozycja.md) — kopia robocza; kanon = PLAN
- [decyzja-operatora-wizja.md](decyzja-operatora-wizja.md) § A/B/C
- [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md) — 49 checkboxów + P0
- [pola-wizja-2026-09.md](pola-wizja-2026-09.md) — tally + tabele O/B0/M10
- [karty-pol-fala-o.md](karty-pol-fala-o.md) · [karty-pol-fala-p.md](karty-pol-fala-p.md) · [karty-pol-fala-t.md](karty-pol-fala-t.md)
- [ai-nauka-i-dowody.md](ai-nauka-i-dowody.md), [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md)
- [docs/state/CURRENT.md](../state/CURRENT.md) — P0 + Fala O + Fala I, plaster 128.0
