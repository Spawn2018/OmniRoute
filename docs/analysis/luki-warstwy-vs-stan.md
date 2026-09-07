# Luki warstw vs `stan-planu-funkcje.md`

**Data:** 2026-09-07.  
**Cel:** czego brak w [stan-planu-funkcje.md](stan-planu-funkcje.md) z czterech warstw (pola / UI / integracje / AI).  
**Nie ruszono** `stan-planu-funkcje.md`. To nie kanon kolejki (`PLAN-REALIZACJA.md` § Kolejka, `CURRENT.md`).

**Werdykt:** `stan-planu` ma **funkcje fal T–V** (47+25+37+35 wierszy) i **tally** (324 pól / 32 tabele / 49 checkboxów / cytat `ai-gdzie-uzasadnione.md`). **Nie ma** inwentarza 32 tabel jako wierszy, **nie ma** osobnych wierszy sześciu powierzchni UI, **nie ma** listy P0 z [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md), **nie ma** list 1/2/3 z [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md).

Legenda: **BRAK** = nie ma wiersza (ani nazwy tabeli/jobu). **WZMIANKA** = nazwa w cudzym wierszu, nie własny wiersz warstwy.

---

## Pola

Źródło: [pola-wizja-2026-09.md](pola-wizja-2026-09.md) § „NOWE (brak tabeli)” — **32 tabele jako wiersze**, nie 324 kolumny.

`stan-planu` § podsumowanie: tally **324 / 32** + zdanie „Nie dump 324 pól w tym pliku”. Karty T1–T5 i T7. **Brak tabeli 32 obiektów.**

### Jest nazwa tabeli (9/32) — w wierszu funkcji, nie jako inwentarz pól

| Tabela | Gdzie w `stan-planu` |
|---|---|
| `stop` | T1 |
| `trip` | T2 |
| `resource` | T2 |
| `entity_event` | B0 |
| `position_event` | V5 jako `PositionEvent` |
| `exchange_message` | V5b |
| `monitoring_scheme` | C1+C7+C8 |
| `party_document` | C1+C7+C8 |
| `postal_dispatch` | F11 |

### BRAK nazwy tabeli (23/32)

Funkcja-sąsiad bywa w sekcji 1; **obiekt z katalogu pól nie istnieje jako wiersz.**

| # | Tabela | Sąsiad w `stan-planu` (nie zastępuje wiersza) |
|---|---|---|
| 1 | `relation_document_requirement` | C8 tylko `party_document` + 409 |
| 2 | `telematics_connector` | V5 lista adapterów |
| 3 | `resource_telematics_link` | — |
| 4 | `weather_observation` | V2 Open-Meteo wzdłuż trasy |
| 5 | `party_exchange_snapshot` | C9 pola scoringu, bez nazwy tabeli |
| 6 | `shipment_monitoring_filing` | C1 SENT+GEO |
| 7 | `map_basemap` | T6+X8 „podkłady”, bez katalogu |
| 8 | `user_map_prefs` | T6+X8 „on/off u usera” |
| 9 | `tenant_map_provider` | T6+X8 „płatne BYO u admina” |
| 10 | `erp_connector` | F9 „Adapter FS+FZ” |
| 11 | `erp_series_map` | — |
| 12 | `erp_export` | — |
| 13 | `scan_enhance_run` | X9 OpenCV |
| 14 | `invoice_match_candidate` | F10 ranking SQL |
| 15 | `network_print_requirement` | D9 409 / wymóg sieci |
| 16 | `document_template` | D9 „szablon = dane” |
| 17 | `shipment_package` | D9 QR `shipment_ref` |
| 18 | `postal_tracking_event` | F11 EN+EPO |
| 19 | `postal_epo` | F11 „imię tylko EPO” |
| 20 | `purchase_invoice` | F10 ingest FV kosztowej |
| 21 | `purchase_invoice_allocation` | — |
| 22 | `quote_engagement` | X7 zdarzenia lejka |
| 23 | `quote_view_token` | X7 „PDF z tokenem” |

T3 `container` jest w `stan-planu` i **nie** jest na liście 32 — to nadmiar wobec katalogu pól, nie luka.

Rozszerzenia istniejących tabel (`charge.source_ref`, `draft_kind`, `shipment_ref`, …) **nie** były w zakresie tego audytu (operator: tabele, nie 324 kolumny). `charge.source_ref` i tak ma własny wiersz P0 leftover.

---

## UI

Zakres: planning board T6, mapa X8, split HITL, lejek X7, wieża V6, canvas `ui-04`.  
Makiety: [docs/design/README.md](../design/README.md), [ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx), [ui-06-vision.canvas.tsx](../design/ui-06-vision.canvas.tsx). Kolejka: [kolejka-propozycja.md](kolejka-propozycja.md) T6 / X7 / X8 / V6.

`stan-planu` rozprawia się z **innym** canvasem (`wizja-plan-decyzja.canvas.tsx` — „NIE, to nie dokument”). **Żaden** wiersz nie cytuje `ui-04-hitl` ani `ui-06-vision`.

| Powierzchnia | W `stan-planu` | Brak jako wizualizacja |
|---|---|---|
| **T6 planning board** | WZMIANKA w jednym wierszu z X8: Timeline/Blocks/Table/Legs | Własny wiersz UI. Z [kolejka-propozycja.md](kolejka-propozycja.md) T6: **select&drop z walidacjami**, **mapa lazy**, **pre-planning**. Karta pól T6 = świadoma luka („tylko zapowiedź UI”) — nadal brak opisu ekranu. |
| **X8 mapa** | Zlany z T6: darmowe on/off, płatne BYO, zakaz `tile.openstreetmap.org`, budżet 250 kB | Własny wiersz mapy. Katalog podkładów (`map_basemap`). Nakładki ruch / LEZ / OpenRailwayMap (są w §2 „Nakładki…”, nie jako UI X8). Atrybucja. P0 OpenFreeMap + GUGiK na powierzchni mapy (w `stan-planu` tylko B#16 / C#17). Instrukcja admina [podklady-map-admin.md](podklady-map-admin.md). |
| **Split HITL** | WZMIANKA w X9+X6: „split HITL” + bbox | Ekran: lewo dokument / prawo pola. Jeden split, `draft.kind` różni job (RFQ / FV / cennik / CMR) — nie nowy ekran. Istniejący `hitl-review-split.tsx`. |
| **X7 lejek** | Wiersz funkcji: `sent` / `pdf_viewed` / `replied` / `converted` + PDF z tokenem | Widok lejka (szczeble, czasy SQL). Zdarzenia z katalogu/`kolejka` **poza** tymi czterema: `email_opened` (jest tylko jako ryzyko Apple MPP), `delivered`, `lost`. Tabele `quote_engagement` / `quote_view_token` (pola). |
| **V6 wieża** | Zlana z V5: jedno zdanie „Wieża: stock→EBITDA” | Własny wiersz wieży. Łańcuch **stock→produkcja→sprzedaż→EBITDA**. „Co jeśli nie zareagujesz” (kolejka V6). Canvas `ui-06-vision` (Watchtower / oś / portale). Early Warning GREEN/AMBER/RED/BLACK jest w §2 jako HZ, nie jako UI V6. |
| **canvas ui-04** | **BRAK** (zero wystąpień `ui-04`) | Makieta [ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx): label Art. 50 zawsze widoczny; pewność per pole; próg 0,7 + disambiguation; accept zbiorczy tylko zaznaczonych; odrzucenie z uzasadnieniem; optimistic accept zakazany; spany na PDF. |

---

## Integracje

Źródło P0: [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md) linia „P0 = …” + nagłówki `###` z **P0**.

`stan-planu` § podsumowanie: **49 checkboxów**, bez listy P0. Adaptery są **spakowane** w V5 / F9 / F11 / D8 / C1.

### P0 — brak własnego wiersza integracji

| P0 z `dostepy` | W `stan-planu` | Luka |
|---|---|---|
| OpenFreeMap | WZMIANKA B#16 / C#17 („Darmowe P0”) | Brak wiersza podkładu P0 w sekcji 1 (X8) |
| GUGiK WMTS | j.w. | j.w. |
| Google ML Kit Document Scanner | WZMIANKA B#25 (plus Scanbota) | X9 = OpenCV; **ML Kit nie jest jobem sekcji 1** |
| Apple VisionKit | ta sama wzmianka B#25 | Para on-device z `dostepy` §11; nie P0 w nagłówku, ale ten sam stos skanu |
| Comarch ERP Optima | F9 „Adapter FS+FZ”; B#20 „Comarch CDN/partner” | Brak wiersza Optima (SOAP/WebAPI + agent) |
| Comarch ERP XL (CDN API) | B#20 | Brak wiersza XL ≠ Optima |
| Symfonia WebAPI | B#20 „Symfonia klucz” | Brak wiersza Symfonia (docs publiczne = kod wolno) |
| Subiekt nexo (Sfera) | B#20 „Sfera nexo≠GT” | Brak wiersza nexo |
| Subiekt GT (Sfera GT) | B#20 | Brak wiersza GT (inny dodatek niż nexo) |
| Palletforce Alliance API | D8 lista sieci (sekcja 3); C#21 odrzut generatora | Brak wiersza P0 Palletforce w sekcji 1 |
| Poczta REST USS 2.0 | F11 „EN + EPO”; B#19 „REST publiczne” | Śledzenie USS nie jest nazwane (osobny kanał vs EN SOAP vs EPO) |

### P0 — tylko nazwa w cudzym wierszu (nie lista integracji)

| P0 | Gdzie | Brak |
|---|---|---|
| GBOX | V5 „P0 PL (…)”; B#9 docs za loginem | Własny wiersz native adaptera (blokuje kod: TAK) |
| IKOL | V5 lista | Własny wiersz (docs publiczne) |
| Flotis REST | V5 lista | Własny wiersz |
| Wialon SDK | V5 lista | Własny wiersz |

### P0 — jest wiersz funkcji (nie brak nazwy)

Open-Meteo (V2), KSeF 2.0 (F1), BDO (C6 / C1), SENT PUESC (C1), Trans.eu Partners (C9), Trans.eu monitoring/trace (V5b), EN SOAP + EPO (F11). Nadal **brak listy P0** jako warstwy — te joby są funkcjami fal, nie inwentarzem dostępów.

---

## AI

Źródło: [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md) listy **1 TAK / 2 NIE / 3 SZARE** (po 12).

`stan-planu` § podsumowanie: **akapit zasad** (TAK HITL extract + liczby DocILE; NIE auton. zapis / LLM-kalkulator / GAN / scoring osoby) + cytat pliku. **Brak trzech tabel jobów.**

### Lista 1 — AI TAK (HITL)

| # | Job | W `stan-planu` |
|---|---|---|
| 1 | Cennik/oferta → kandydaci `amount_text` / `unparsed_regions` | BRAK wiersza (tylko zasada w podsumowaniu) |
| 2 | `inbound_message` → ten sam `extract_to_draft` | BRAK |
| 3 | Mail → szkic RFQ / pól zlecenia | BRAK (Ocean Email AI w §2 to inny job) |
| 4 | FV kosztowa → `extraction_draft` kind=`purchase_invoice` | WZMIANKA F10 ingest; **brak `draft_kind`** |
| 5 | Skan CMR/POD **bez** kodu Omni | WZMIANKA X9+X6 |
| 6 | Jeden split HITL, `draft.kind` różni job | BRAK (X9 = skan, nie jeden UI na 4 kindy) |
| 7 | `bbox` + pewność 0–1 + `span_text` + `operator_override` | CZĘŚĆ: bbox w X9; brak span/pasma/override |
| 8 | Klasyfikacja `document_kind` gdy brak QR | BRAK (D9: HITL bez kodu ≠ klasyfikacja kind) |
| 9 | Diff pól vs zlecenie (X6) | WZMIANKA „diff CMR” |
| 10 | Szkic `mail_draft` „podaj `shipment_ref` / kontener” | BRAK |
| 11 | Label „propozycja AI” / Art. 50 / `U-art50` | **BRAK** (zero `Art. 50` / `U-art50`) |
| 12 | Guard regex; llm-guard + Presidio = cel HC | BRAK |

### Lista 2 — AI NIE

Część zasad jest w §4 (C#16 RAG, C#19 auto-zapis/accept, C#20 GAN, C#6 scoring JDG) i w F10 (XML FA(3) bez LLM, nigdy auto-link). **Brak tabeli 12 zakazów.**

| # | Job | Luka vs lista 2 |
|---|---|---|
| 1 | Sumy / marża / VAT / kurs w modelu | Zasada w podsumowaniu; nie wiersz listy 2 |
| 2 | Auto-zapis extractu / `rate_line` / `charge` | C#19 — jest jako odrzut, nie jako wiersz listy 2 |
| 3 | Sell / marża z LLM | BRAK osobno (HC-03 przy T4 / C#22) |
| 4 | Auto-podpięcie FV | F10 „Nigdy auto-link” |
| 5 | Score dopasowania FV / suma linii **w modelu** | BRAK (F10 mówi ranking SQL, nie „AI NIE score”) |
| 6 | Parser KSeF FA(3) przez LLM | F9/F10 „XML FA(3) bez LLM” |
| 7 | Auto-zapis skanu gdy **jest** kod Omni / LLM zamiast skanera | BRAK (D9: HITL gdy brak kodu; cisza że tor QR = SQL bez LLM) |
| 8 | Auto-scoring osoby / JDG | C#6 |
| 9 | GAN / inpainting glifów | C#20 |
| 10 | Accept bo pewność / optimistic UI | C#19 + X9 |
| 11 | RAG na wycenie / VAT / schemacie DB | C#16 |
| 12 | Numer nadania / imię EPO z OCR koperty; znaczek z LLM; scraping PP | CZĘŚĆ: C#24 imię bez EPO; **brak** „AI NIE OCR koperty / koszt znaczka z LLM” |

### Lista 3 — SZARE

V1 ledger + V2 ETA pokrywają **szare #1** jako funkcje fal, nie jako wiersze listy 3. Reszta: **BRAK** albo inna nazwa w §2/HZ.

| # | Job | W `stan-planu` |
|---|---|---|
| 1 | ETA / slot + ledger, LLM nie liczy ETA | V1+V2 (funkcja, nie lista 3) |
| 2 | AI summaries wątków mailowych | BRAK |
| 3 | Chat → reguła walidacji | BRAK |
| 4 | Czat o rekordach / copilot wieży (M-57) | BRAK |
| 5 | Agent zakupowy (RFQ→ranking, award HITL) | BRAK (nie mylić z Dispatch / Ocean Email AI w §2) |
| 6 | Narracja CFO / raport po SQL (M-15) | BRAK |
| 7 | Anomalia / fraud jako flaga do recenzji ≠ werdykt | BRAK (odrzut = scoring osoby, nie szara flaga M-54) |
| 8 | Ryzyko kontrahenta / early warning zarządu | WZMIANKA §2 Early Warning V6 (słownik statusów, nie job listy 3) |
| 9 | Contract intelligence (FV vs umowa) | BRAK w tabelach; HZ odroczone w stopce §4 |
| 10 | Negocjacje w limitach ceny/marży | WZMIANKA stopka §4 „autonomous negotiation” |
| 11 | SQL z modelu przez `sqlglot` | BRAK |
| 12 | Digital twin / Omni Market forecasts | WZMIANKA stopka §4 „digital twins pełne” |

---

## Licznik braków (wiersze warstwy, których nie ma)

| Warstwa | Wymagane jako wiersze | W `stan-planu` jako ta warstwa | Brak |
|---|---|---|---|
| Pola (32 tabele) | 32 | 0 inwentarza; 9 nazw w funkcjach | **23 nazwy + cała tabela 32** |
| UI (6 powierzchni) | 6 | 0 osobnych wierszy UI; 3 funkcje zlane (T6+X8, X9 split, X7, V5+V6) | **ui-04 w całości**; T6/X8/V6/split jako ekrany |
| Integracje P0 | 22 nagłówki `**P0**` w `dostepy` | 0 listy P0; ~7 funkcji pokrywa nazwę | **OpenFreeMap, GUGiK, ML Kit, VisionKit, 5× ERP, Palletforce, USS**; 4× GPS PL bez własnego wiersza |
| AI listy 1/2/3 | 36 jobów | 0 tabel list; akapit zasad + część odrzuceń | **lista 1: 1–3, 8, 10–12**; **lista 2: 5, 7, 12 (OCR/znaczek)**; **lista 3: 2–7, 9, 11** |

---

## Źródła (czytane)

- [stan-planu-funkcje.md](stan-planu-funkcje.md)
- [pola-wizja-2026-09.md](pola-wizja-2026-09.md) § NOWE 1–32
- [dostepy-do-zdobycia.md](dostepy-do-zdobycia.md) P0
- [ai-gdzie-uzasadnione.md](ai-gdzie-uzasadnione.md) §1–3
- [kolejka-propozycja.md](kolejka-propozycja.md) T6, X7, X8, V6
- [docs/design/ui-04-hitl.canvas.tsx](../design/ui-04-hitl.canvas.tsx)
