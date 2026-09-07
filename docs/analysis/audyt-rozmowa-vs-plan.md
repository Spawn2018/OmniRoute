# Audyt: rozmowa (transkrypt) vs plan analizy

**Data audytu:** 2026-09-07  
**Werdykt metody:** zero marketingu, zero zgadywania. Źródło = ścieżka + cytat.  
**Transkrypt:** `C:\Users\sebas\.cursor\projects\d-OMNIROUTE\agent-transcripts\2db73c11-b1f8-44d1-947a-79a8402254aa\2db73c11-b1f8-44d1-947a-79a8402254aa.jsonl`  
**Zakres tabeli:** tematy z listy operatora (telematyka → pola). Nie audytuje tu całego PDF ChatGPT ani Qargo/SPEED (to `inwentarz-mc-pdf.md`).

## Definicje werdyktu

| Werdykt | Warunek |
|---|---|
| **WCIELEONE** | Decyzja z rozmowy jest w matrycy **i** ma ID w `kolejka-propozycja.md` **i** ma nazwane pola/tabele w §13 (albo w karcie knowledge). Brak wiersza w `karty-pol-fala-t.md` jest odnotowany w kolumnie „Pola”, ale sam plik kart **odsyła** fale D/P/X/F/C/V do `/plan-modul` — to nie kasuje wcielenia decyzji. |
| **CZĘŚĆ** | Jest w matrycy, ale: sprzeczność z kolejką, brak wiersza kolejki, albo kolejka obiecuje więcej niż matryca (TO_VERIFY). |
| **BRAK** | Rozmowa ma decyzję; plan milczy **i** nie odrzuca. |

**Pola w planie?** osobna kolumna: `karty-pol-fala-t.md` ma **tylko T1–T5 i T7**. Żadne z nazw `PositionEvent`, `quote_engagement`, `paper_post`, `purchase_invoice`, `party_document`, `monitoring_scheme`, `postal_dispatch`, `user_map_prefs` w tym pliku **nie występuje** (grep 2026-09-07).

## Kanon (nie edytowany)

- `docs/state/CURRENT.md`: **Etap: Plan**; **Faza: Fala S — named parks**; „Następny: named parks (Auth0 S53, portale S55, AIS wieży). `/noc` pomija.”
- `docs/PLAN-REALIZACJA.md` § Kolejka: po Q-E4 → Fala S named parks. **Brak** fal T/D/P/X/F/C/V z analizy. `F11.0` w PLAN = M-68 Obserwowalność (plaster 48.0) — **to nie jest** F11 książki nadawczej z propozycji.
- `docs/analysis/kolejka-propozycja.md` linia 3: „**To nie jest kanon.** Kanon kolejki = PLAN-REALIZACJA.md § Kolejka realizacji.”

Analiza **nie jest wpięta** w kolejkę kanonu. `/noc` jej nie buduje.

## Operator miał rację (fakt historyczny)

W transkrypcie operator wielokrotnie stwierdza, że pomysł pada w czacie, a nie ląduje w planie:

- MSG#9 (linia 97): „Dalej nie widzę żebyś zastosował wszystko […] Jeżeli to było celowe to chce powód dlaczego odrzucamy.”
- MSG#15 (linia 143): „chyba jednak nie wdożyłeś albo odrzuciłeś z podaniem powodu wszystkiego”
- MSG#28 (linia 237): „Widze, że wpadamy na pomysł ale nie realizujesz go. […] Przez realizację rozumiem dodanie do planu. mnasz mi dodać pola”

**Stan po wieczorze 2026-09-07:** tematy z listy poniżej **są dopisane** do matrycy §13g–13p + kolejki-propozycji + kart knowledge 006–011. Luki, które **zostały**, to: (1) sprzeczności matryca↔kolejka, (2) karty pól tylko Fala T, (3) TO_VERIFY sprzedawane w kolejce jak pewnik.

---

## Tabela audytu

| Temat | W rozmowie | W matrycy/kolejce (cytat/sekcja) | Pola w planie? | Luka | Werdykt |
|---|---|---|---|---|---|
| Telematyka: zero własnego HW | MSG#11/12 linia 107/111: „nie robimy własnychurzadzeń. wchodzimy w teltonika i quecklink.” | Matryca §9: „Telematyka: **bez własnych urządzeń** — Teltonika + Queclink […] KOPIUJ — §13g \| V5 + V5b”. Rejestr: „Własne urządzenia GPS […] ODRZUCONE na stałe (biznes)”. Kolejka V5: „zero własnego HW”. Karta `docs/_knowledge/market/006-telematics-hub.md`. | Nazwa decyzji: tak. Kolumny HW: niepotrzebne (zakaz). | — | **WCIELEONE** |
| Teltonika + Queclink (pakiet Omni, nie produkcja) | Ten sam MSG#11. Inwentarz MC §4 → MAT §13g. | §13g: „urządzenia **Teltonika** i **Queclink** (nie produkujemy; instalacja u przewoźnika, który chce). Protokoły z wiki producentów — TO_VERIFY per model.” Kolejka V5: „L1a (Teltonika+Queclink)”. | Brak karty pól modeli/protokołów. V5 w kolejce. | TO_VERIFY per model; brak listy SKU w karcie pól. | **WCIELEONE** |
| Omni Telematics Hub (`PositionEvent`, warstwy L0–L1c) | MSG#11: „Musimy znaleźć sposób jak to zintegrować […] brać dane po API zewnętrznch dostawców gdy przewoźnik poda nam dane dostępowe do API i numer rejestracyjny” | §13g: „jeden **Omni Telematics Hub**. Normalizuje pozycję do `PositionEvent`”. Kolejność: pakiet Omni → BYO API → aggregator Linkway/DRIP → giełda → driver app. Kolejka V5: „`PositionEvent` + adaptery L0 / L1a / L1b / L1c”. | `PositionEvent` nazwane w §13g i V5. **Brak** tabeli kolumn w `karty-pol-fala-t.md`. §13j: „Unified Telemetry Model (pola: position, fuel, driver, CAN, DTC, temp, source) […] KOPIUJ — kontrakt V5” — nie zlane z kartą V5. | Unified Telemetry ≠ karta pól. | **WCIELEONE** |
| Okno obserwacji związane z `trip` (default 3 dni) | MSG#11: „gdy dane auto […] nie będzie wykonywać już transportów to po okreslonym czasie np. 3 dni przestanie być obserwowane […] połączyć jakoś ze zleceniami.” | §13g: `trip.assigned(vehicle)` → start; `last_stop.completed` → grace N dni (domyślnie 3, M-03); live gaśnie, historia w `entity_event`. Kolejka V5: „okno obserwacji związane z `trip` (start przy przypisaniu, stop po last_stop + N dni, domyślnie 3)”. Karta 006: to samo. | Pole `grace` = M-03, nie kolumna w karcie T2. T2 ma `vehicle_id` / status — karta T2 **nie** opisuje poll/stop telematyki. | Karta T2 nie wiąże `resource` z oknem V5. | **WCIELEONE** |
| Adaptery P0 PL: GBOX / IKOL / Flotis / Wialon | MSG#11: „POszukaj wszystkich polskich providerów […] oraz 30 najwiekszych europejskich. Nastepnie wyszukaj ich api.” | **Matryca §13g:** „Adaptery P0: GBOX + IKOL + Flotis + Wialon”. Karta 006: „P0 adaptery PL: IKOL […] Flotis […] GBOX […] Wialon SDK.” **Kolejka HZ:** „kolejne adaptery GPS **poza P0** (GBOX/IKOL/Flotis/Wialon)”. V5 wymienia L1a Teltonika, L1b BYO, L1c aggregator — **bez** tych czterech nazw. | Brak karty pól credentiali adaptera. | **Sprzeczność P0 vs HZ.** Matryca i karta = P0; kolejka = HZ. | **CZĘŚĆ** |
| Tronik (ATRAX4) | MSG#16 linia 155: „a co z dostawcą telematyki tronic i logisat?” | §13g: „**Tronik** (`tronik.pl`, platforma **ATRAX4** […]). Publicznego swaggera nie ma — API/connector po umowie.” Jest na Linkway jako ATRAX4. | Brak. | **Brak wiersza kolejki** (nie V5c, nie P0). Ścieżka tylko: umowa albo L1c. | **CZĘŚĆ** |
| Logisat | Ten sam MSG#16. | §13g: „**Logisat** […] REST API + dokumentację «na życzenie»; […] konektory **Linkway** i **CO3**. Native adapter po dokumentacji; do tego czasu aggregator.” | Brak. | Jak Tronik: matryca tak, kolejka milczy o nazwie. | **CZĘŚĆ** |
| Giełdy GPS (Trans.eu / TIMOCOM / Transporeon / Teleroute) | MSG#11: „przeszukaj informacji na transporeon, timocom, trans.eu, teleroute jak można wymorzystać te platformy aby móc śledzić transport” | §13g tabela: Trans.eu `…/monitoring`+`/trace`; TIMOCOM Tracking API; Transporeon Open Visibility; Teleroute = CRUD ofert, visibility = osobny produkt. Kolejka V5b: „Widoczność giełd per transport (Trans.eu monitoring/trace, TIMOCOM Tracking, Transporeon Open Visibility) […] Teleroute = oferty, nie GPS”. | Brak karty pól `exchange_visibility`. V5b w kolejce. | Umowy TO_VERIFY — zapisane, nie ukryte. | **WCIELEONE** |
| Zakaz scrapingu czatów giełd | MSG#11: „kontrolowoać rozmowy na tych giełdach […] stawki […] na komunikatorach wewnetrznych” | Rejestr: „Podsłuch / scraping komunikatorów giełd […] gdy nie jesteśmy stroną […] Art. 267 KK + RODO + ToS […] ODRZUCONE na stałe (prawo)”. Wolno: tenant jest stroną → `exchange_message` → HITL → `rate_line`. Diagnostyka bez podsłuchu: accepted price + `quoted_amount` na M-30 + metryki jobu. V5b: „zakaz scrapingu czatów”. | `exchange_message`, `quoted_amount` nazwane. Brak karty pól. | — | **WCIELEONE** |
| Trans.eu Partners API (scoring + opinie słowne) | MSG#13 linia 121: „Dodaj weryfikację opinii z trans.eu na temat przewoxników - scoring oraz opinie słowne.” | §13h: `GET /ext/partners-api/v1/partners/{id}` → `overall_rating`, satisfaction, `trans_risk`, `documents.expire_date`. „Opinie słowne **są na platformie** […] **Publicznego endpointu listy komentarzy nie ma** — TO_VERIFY u `api@trans.eu`.” Rejestr: scraping opinii ODRZUCONE. **Kolejka C9:** „Snapshot Trans.eu: `overall_rating`, satisfaction, TransRisk **+ opinie słowne po oficjalnym API**”. | Snapshot nazwane w §13h. Brak karty pól. | Kolejka C9 pisze opinie słowne jak pewnik; matryca mówi: endpointu nie ma. | **CZĘŚĆ** |
| Pogoda Open-Meteo, cała Europa | MSG#13: „prognoza pogody musi byc w całej europie nie tylko w PL”. MSG#8 linia 91: „Co z SENT, […] pogodą […] opłatami drogowymi.” | §13h: „Źródło bazowe: **Open-Meteo** […] Pobór wzdłuż geometrii `trip` […] IMGW / DWD / Météo-France = suplement”. Kolejka V2: „pogoda Open-Meteo **wzdłuż trasy w całej Europie**”. Karta 007. Matryca §9 wiersz pogoda. | Brak tabeli punktów/odcinków w karcie pól. | — | **WCIELEONE** |
| BDO / KPO / DIWASS | MSG#13: „dodaj obsługe odpadów BDO w ruchu krajowym i międzynarodowym.” | §13h tabela: PL BDO+KPO REST `bdo.mos.gov.pl`, zmiana API 1.01.2027; UE DIWASS od 21.05.2026 (WSR 2024/1157). Kolejka C6: „Odpady: BDO/KPO kraj + DIWASS/WSR transgranica”. Karta 007. | Numery BDO/KPO nazwane w §13h. Brak karty pól. | — | **WCIELEONE** |
| Blokada `shipment` na polisę / składkę / licencję | MSG#13: „blokade zakłądania zleceń gdy wygaśnie polisa albo będzie nieopłacona składka albo wygaśnie licencja […] Odblokowanie po ponownym dodaniu aktualnych dokumentów.” | §13h: tabela `party_document`; 409 przy `POST shipment`; odblokowanie = nowy wiersz. Kolejka C8: „`party_document` + blokada `POST shipment` (polisa / składka / licencja)”. Matryca §13c analogiczny wiersz. | §13h wymienia: `kind` (`ocp`/`ocs`/…), `valid_from`/`valid_to`, `premium_status` (`paid`/`unpaid`/`unknown`), `source_ref`. **Brak** w `karty-pol-fala-t.md`. T2 ma tylko „document_expiries” ogólnie. | Zestaw wymaganych dokumentów = M-03 — nie rozpisany per relacja w karcie. | **WCIELEONE** |
| SENT-EU: katalog, nie klon w każdym kraju | MSG#13: „dodaj wszystkie systemy podobvne do Polskiego Sent w każdym kraju w EUROPIE.” MSG#8: „Co z SENT”. | §13h: „Większość krajów UE **nie ma** klona SENT”. Model `monitoring_scheme`. Unia: EMCS, NCTS, e-TIR, DIWASS, eFTI. Naród potwierdzony: SENT, EKAER, BIREG, RO e-Transport, Trackdéchets, RENTRI, SILICIE, ATLAS. SK/CZ/AT/…: **brak potwierdzonego klona**. Rejestr: „Wymyślanie SENT-ów […] ODRZUCONE na stałe”. Kolejka C1 SENT+GEO; C7 katalog. | `monitoring_scheme` nazwane. Brak karty pól. | Operator chciał „wszystkie kraje”; plan **odrzuca wypełnianie mapy**. To wcielenie uczciwe + ODR, nie BRAK. | **WCIELEONE** |
| Myto precyzyjne EU/EFTA | MSG#13: „Opłaty drogowe muszą być precyzyjne i działać w każdym europejskim kraju.” MSG#8: „dokłądnymi opłatami drogowymi.” | §13h: „Nie ma jednego darmowego rządowego API na całą UE.” Geometria + pojazd + data; winieta ≠ km. PTV/HERE/NAPSPAN/TollCalc; taryfy publiczne. Brak taryfy = warning. Kolejka V2b: „Toll engine EU/EFTA: klasa/osie/emisja/CO₂/data; winieta osobno; `charge` z `source_ref`”. | Klasa/osie/emisja nazwane w V2b/§13h. Brak karty pól na `resource`. T2 ma `vehicle_profile`, `capacity_*`, `adr_certified` — **nie** osie/Euro/klasa CO₂. | Pola pojazdu pod myto nie są w karcie T2. | **WCIELEONE** |
| Lejek oferty (mail/PDF/odpowiedź/konwersja) | MSG#14 linia 130: czasy sent→otwarcie maila, sent→PDF, sent→odpowiedź, PDF→odpowiedź, konwersja. (Napis urwany na „ę kiedy klient…”) | Matryca §1: „Lejek oferty: […] KOPIUJ — §13i \| X7”. §13i tabela zdarzeń + 5 czasów SQL. Kolejka X7: „`quote_engagement` (sent / email_opened / pdf_viewed / replied / converted)”. Karta 008. Rejestr: piksel bez zgody ODRZUCONE. | Zdarzenia nazwane w §13i. Brak w `karty-pol-fala-t.md`. | `delivered` TO_VERIFY per skrzynka. | **WCIELEONE** |
| Mapy: wiele darmowych u usera + BYO API u admina | MSG#17 linia 162: „wyboru wielu darmowych podkładów map […] w ustawieniach uzytrkownika […] administrator […] podpięcia jak najwięcej płatnych podkładów […] po podaniu swojego api […] instrukcja” | §13k: `user_map_prefs` + `tenant_map_provider`; lista darmowych P0; lista płatnych BYO; zakaz `tile.openstreetmap.org`. Kolejka X8 + T6 „podkłady z §13k”. Plik `docs/analysis/podklady-map-admin.md` (instrukcja admina, skąd klucz). Karta nie 006–011 — osobny plik analizy. | `user_map_prefs`, `tenant_map_provider` w §13k. Brak karty w `karty-pol-fala-t.md`. T6: „pola pochodne, osobna karta UI przy Planie”. | Carto/Esri limity TO_VERIFY. | **WCIELEONE** |
| ERP FS+FZ; KSeF tylko Omni | MSG#18 linia 171: Comarch, Symfonia, Subiekt. MSG#19 linia 179: „Faktury wystawia omni, wysyłamy do systemów księgowych faktury kosztowe i przyhcodowe”. | §13l: „faktury **wystawia Omni** (KSeF = Omni, nie ERP)”. Tabela: przychodowa → FS; kosztowa → FZ. `ksef_issuer` = `omni` na stałe. Kolejka F9. Plik `docs/analysis/erp-fk-adapter.md`. Rejestr: podwójny KSeF ODRZUCONE; SQL `sa` ODRZUCONE. | `purchase_invoice`, `erp_connector` nazwane. Brak karty pól. | P1 enova/WAPRO = kolejka po P0, nie BRAK. | **WCIELEONE** |
| FV kosztowe: mail / KSeF / skan + HITL + drabina + `shipment_ref` | MSG#20/21 linia 185/188: zaciąganie z maili, KSeF, skanów; podpięcie po człowieku; rozpoznanie zlecenia; faktury z innych kontynentów. | §13m: trzy źródła → `extraction_draft` kind=`purchase_invoice`; drabina 1–6 SQL; nigdy auto-link; `shipment_ref` na wychodzących zleceniach. Kolejka F10. Rejestr: auto-podpięcie ODRZUCONE. | Drabina i `shipment_ref` w §13m. Brak karty pól. | Progi M-03 nie rozpisane liczbowo (poza opisem 1 vs 2–8 vs 0). | **WCIELEONE** |
| Wydruki sieci drobnicowych + skan QR na zlecenie | MSG#22 linia 191: druk dokumentu sieci; skan i podpięcie pod przesyłkę/zlecenie. | §13n: `network_print_requirement` + `document_template` + skan; QR `shipment_ref` na każdym druku; nasz kod → zapis od razu; bez kodu → HITL. Kolejka D9, D2. Karta 009. Rejestr: udawanie Palletforce ODRZUCONE; auto-skan bez kodu ODRZUCONE. | Nazwane w §13n. Brak karty pól (D poza Falą T). | Etykieta obcej sieci = D8 + umowa. | **WCIELEONE** |
| Enhance skanu: OpenCV, ML Kit, zakaz GAN; split HITL | MSG#23 linia 202: upscaling, kadr, split lewo dokument / prawo pola+pewność+edycja. MSG#25 linia 220: „jakby ktoś trzymał oryginał […] skaner”. | §13o: ML Kit / VisionKit; OpenCV warp/deskew/biel/~300 DPI Lanczos; **zakaz** Real-ESRGAN/GFPGAN/inpainting. Split bbox + `confidence` + `operator_override`. Kolejka X9. Karta 010. Rejestr GAN ODRZUCONE; accept bez kliknięcia ODRZUCONE. Matryca §10 Document Intelligence → X6+X9. | `ExtractedField` / bbox nazwane w §13o. Brak karty. M-20 split istnieje (CZĘŚĆ w matrycy — brak bbox). | P1 UVDoc = A/B, nie wymóg. | **WCIELEONE** |
| Książka nadawcza PP: EN + REST + EPO + skaner USB + `paper_post` | MSG#24 linia 211: książka, PP, kod kreskowy, kto odebrał. MSG#26 linia 225: API vs numer, skaner. MSG#27 linia 230: „faktura będzie papierowa twedy = poczta polska”. | §13p: `postal_dispatch`; EN SOAP + REST `checkmailex`; imię tylko EPO `getEPOStatus`; USB/HID; kolejność numeru 1 EN / 2 skan / 3 wklejenie. `sales_invoice.delivery_channel`: `electronic` \| `paper_post`. Papier **nie** wyłącza KSeF. Kolejka F11. Karta 011. Rejestr: scraping PP ODRZUCONE; obietnica „kto” bez EPO ODRZUCONE. | `paper_post`, `numer_nadania`, `postal_dispatch` w §13p. Brak w `karty-pol-fala-t.md`. | Umowa EN/EPO — nie w kolejce jako TO_VERIFY checkbox. | **WCIELEONE** |
| Pola systemu (każdy moduł: kolumny do wpisania i zapisu) | MSG#3 linia 25: „w każdym module […] konkretne pola […] zapisać te dane na stałe”. MSG#6 linia 79: „Czy zapełniłeś każdy moduł dokładnymi polami”. MSG#28: „masz mi dodać pola które będą używane systemie do wszystkiego o czym pisalismy”. | `karty-pol-fala-t.md`: T1 `stop`, T2 `trip`+`resource`, T3 `container`, T4 podzlecenie, T5 `task`, T7 kurs. Linia 128–130: „Fale D/P/X/F/C/V **dostaną karty pól analogicznie przed swoim `/plan-modul`**”. Matryca linia 297: „Karty pól — przy `/plan-modul` (ADR-0004), **nie tu**.” Inwentarz: „Pola […] wchodzą do kart przy `/plan-modul` — nie dublujemy tu 400 kolumn.” | **TAK** Fala T (T1–T5, T7). **NIE** jako tabele: V5, V2/V2b, C6–C9, X7–X9, F9–F11, D9, T6. Tematy wieczorne mają nazwy pól w §13g–p, nie w pliku kart. | Operator żądał kart teraz. Plan **odkłada** je do `/plan-modul`. To nie jest milczenie, ale też nie jest dostarczenie. | **CZĘŚĆ** |

---

## Liczby

| Werdykt | Ile | Tematy |
|---|---|---|
| **WCIELEONE** | **18** | zero HW; Teltonika+Queclink; hub; okno trip; giełdy GPS; zakaz scrapingu czatów; Open-Meteo; BDO/KPO/DIWASS; blokada polisy; SENT-EU katalog; myto; lejek oferty; mapy; ERP FS+FZ/KSeF Omni; FV kosztowe; wydruki+QR; enhance/OpenCV; książka PP |
| **CZĘŚĆ** | **5** | GBOX/IKOL/Flotis/Wialon (P0 vs HZ); Tronik; Logisat; Trans.eu opinie słowne (C9 vs §13h); pola systemu (karty tylko T) |
| **BRAK** | **0** | — |

23 tematy z listy. Żaden z tej listy nie jest dziś nieobecny w matrycy (albo w rejestrze odrzuceń).

---

## Luki do dociągnięcia (pola, fale, odrzucenia)

Konkret, nie „dopisać kiedyś”:

1. **Rozstrzygnąć GBOX / IKOL / Flotis / Wialon:** albo P0 native w V5 (zgodnie z §13g i kartą 006), albo HZ (zgodnie z kolejką). Dziś oba naraz.
2. **V5 w kolejce nie wymienia nazw P0 PL** — tylko L1a Teltonika, L1b BYO, L1c aggregator. Zsynchronizować z §13g.
3. **Tronik ATRAX4:** dodać wiersz kolejki (np. „L1c Linkway ATRAX4 / native po umowie”) albo wpis w HZ z checkboxem umowy. Dziś tylko §13g.
4. **Logisat:** to samo (Linkway + CO3 do czasu dokumentacji).
5. **C9 vs §13h:** kolejka obiecuje „opinie słowne po oficjalnym API”; matryca: endpointu listy komentarzy nie ma. Albo C9 uciąć do scoringu + TO_VERIFY, albo checkbox „mail do api@trans.eu”.
6. **Karta pól V5:** kolumny `PositionEvent` + Unified Telemetry z §13j (position, fuel, driver, CAN, DTC, temp, source) + sekrety adaptera (HC-05) + `trip_id` okna.
7. **Karta T2:** osie, DMC, Euro, klasa CO₂ (wejście V2b myto); powiązanie `resource` ↔ okno V5.
8. **Karta C8:** `party_document` (kind, daty, `premium_status`) — dziś tylko proza §13h + ogólnik `document_expiries` w T2.
9. **Karta C6:** `bdo_number`, id KPO/KPOK, ref DIWASS, flaga nakładki SENT.
10. **Karta C7:** `monitoring_scheme` (kraj, urząd, API, GEO tak/nie).
11. **Karta V2:** punkty Open-Meteo wzdłuż geometrii `trip` (nie jeden kraj).
12. **Karta V2b:** winieta vs km jako dwa rodzaje `charge`; `source_ref` taryfy.
13. **Karta X7:** `quote_engagement` + `tracking_consent` na `party_contact`.
14. **Karta X8:** `user_map_prefs`, `tenant_map_provider`.
15. **Karty F9 / F10 / F11:** `purchase_invoice`, `erp_connector`, `ksef_issuer`; drabina F10; `paper_post` + `postal_dispatch` + `numer_nadania`.
16. **Karty D9 + X9:** `network_print_requirement`, `document_template`; `ExtractedField` bbox/pewność/`operator_override`.
17. **T6:** w `karty-pol-fala-t.md` jest tylko zapowiedź „osobna karta UI” — brak.
18. **Umowa EN/EPO Poczty Polskiej** nie ma wiersza TO_VERIFY w kolejce (F11 zakłada API).
19. **Teltonika/Queclink TO_VERIFY per model** — brak checklisty SKU.
20. **30 EU providerów** (§13g): native = TO_VERIFY; kolejka nie ma P1 listy (Webfleet.connect, Geotab, …).

Odrzucenia z tej rozmowy **są** w rejestrze (własny HW, scraping czatów, scraping opinii, piksel bez zgody, SENT-y wymyślone, GAN, auto-link FV, auto-skan bez QR, podwójny KSeF, scraping PP). Nie ma luki „brak ODR” dla tych tematów.

---

## Co ten audyt świadomie pomija

Tematy z **wcześniejszej** części tej samej rozmowy (bliźniak B0, dedup NIP, role kontrahenta, przetargi §13f, traffic/zakazy jazdy §13d, widok drobnica vs FTL, chatbot klienta) **nie są** w tabeli powyżej — nie było ich na liście operatora do tego audytu. Ich obecność w matrycy = `inwentarz-mc-pdf.md` + §13a–13f/13j, nie ten plik.
