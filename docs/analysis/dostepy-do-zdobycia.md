# Dostępy do zdobycia — wizja 2026-09-07

**Weryfikacja:** 2026-09-07, tylko oficjalne strony (fetch URL).  
**Zakres:** telematyka, pogoda, BDO, SENT, myto, mapy, ERP, KSeF, Poczta Polska (EN / śledzenie / EPO), Trans.eu, giełdy GPS, Palletforce/sieci, ML Kit.  
**Nie commituj. Nie CURRENT. Nie PLAN.**

**HC (nie negocjuj):** sekrety tenanta szyfrowane kluczem tenanta, nigdy w logach/promptach; każde wywołanie zewnętrzne idempotentne; **zakaz scrapingu** (śledzenie PP, giełdy, czaty, portale sieci). Jeśli pole nie jest w docs — `TO_VERIFY`, nie zmyślać endpointu.

**Legenda „Blokuje kod?”**

| Wartość | Znaczenie |
|---|---|
| **NIE** | Jest publiczna specyfikacja — można pisać klienta / adapter. Produkcja i tak dostanie sekrety tenanta (HC-05). |
| **TAK** | Bez umowy, loginu do docs albo sandboxa nie da się domknąć klienta (brak publicznego kontraktu albo docs za loginem). |

**P0** = adaptery / kanały z decyzji operatora 2026-09-07 (benchmark §13g–13p): GBOX, IKOL, Flotis, Wialon, Open-Meteo, BDO, SENT, Trans.eu (partners + monitoring), KSeF, EN + REST śledzenia + EPO, OpenFreeMap + GUGiK, Comarch Optima/XL, Symfonia, Subiekt nexo/GT, Palletforce, ML Kit.

---

## Publiczne — wolno kodować bez umowy

Specyfikacja jest na stronie. Kod klienta nie czeka. Live i tak idzie na sekretach tenanta albo darmowym kluczu self-serve.

- Open-Meteo (docs publiczne; **SaaS Omni = użycie komercyjne** → abonament albo self-host AGPL — poz. 1)
- IMGW dane publiczne, DWD Open Data, portal API Météo-France (suplement, nie baza)
- KSeF API 2.0 (OpenAPI + TEST/DEMO/PRD)
- BDO REST (swagger test; klucze po formularzu integratora — poz. 7)
- SENT: XSD i spec kanałów na PUESC (konto webservice osobno — poz. 8)
- EKAER XML, RO e-Transport (ANAF PDF)
- IKOL, Flotis REST, Wialon Remote API
- Teltonika Codec (wiki)
- Trans.eu: opublikowane endpointy Partners + monitoring/trace (klucze aplikacji osobno — poz. 14–15)
- Teleroute: CRUD ofert fracht/pojazd (`api-docs.teleroute.com`) — **nie** visibility
- OpenFreeMap, GUGiK WMTS, OpenTopoMap / CyclOSM / HOT (atrybucja; **nie** `tile.openstreetmap.org`)
- ML Kit Document Scanner (on-device), VisionKit iOS
- Poczta: PDF WebAPI w96 + REST USS (konto demo śledzenia; EN produkcja = umowa — poz. 28–30)
- Symfonia WebAPI (docs publiczne; live = instancja tenanta)
- HERE Routing v8 OpenAPI, PTV Developer (toll w Routing), NAPSPAN, Geotab SDK, WEBFLEET.connect PDF
- Carto basemaps: klucz self-serve (fair use; komercja TO_VERIFY)

## Czeka na dostęp

Bez tego nie ma sandboxa albo pełnego kontraktu API.

- **P0** GBOX — docs.gbox.pl za loginem
- **P0** Trans.eu — `client_id` / `client_secret` / Api-key (formularz + weryfikacja)
- **P0** BDO — zgłoszenie integratora (klucze test)
- **P0** SENT — webservice PUESC (`projektsent.ias.zielonagora@mf.gov.pl`)
- **P0** Poczta EN — umowa + konto test `en-testwebapi`
- **P0** EPO — usługa na umowie EN
- **P0** Palletforce (i analogicznie Palletline / Alliance) — brak publicznego generatora etykiet
- **P0** Comarch Optima / XL — licencja integracji + agent; brak jednego publicznego REST
- **P0** Subiekt nexo / GT — Sfera (COM), nie publiczny REST
- TIMOCOM / Transporeon Visibility — credentials od AM / Visibility Hub
- Linkway INTEGRATOR / DRIP — umowa agregatora
- DIWASS — rejestracja operatora + Helpdesk KE po GUI
- Queclink Air Interface — PDF nie jest publicznym swaggerem
- Open-Meteo **customer-api** — płatny plan (produkt komercyjny)
- Reszta GPS PL (Cartrack, Navifleet, Tronik ATRAX4, Logisat, …) — docs na życzenie

---

## 1. Pogoda

### - [ ] Open-Meteo — baza pan-EU **P0**

- **Cel:** Prognoza wzdłuż geometrii `trip` (punkty), nie jeden kraj załadunku. Wynik = `entity_event`, nie liczba z LLM.
- **Co zrobić:** Docs publiczne. Produkt Omni jest komercyjny: [Terms](https://open-meteo.com/en/terms) zabraniają free API do komercji. Stripe na [Pricing](https://open-meteo.com/en/pricing) **albo** self-host (kod AGPLv3). Kontakt: `info@open-meteo.com`.
- **Co dostaniemy:** Hosted: klucz + `customer-api.open-meteo.com` (`apikey=`). Free: `api.open-meteo.com/v1/forecast` bez klucza, limit 10k/dzień, **nie** do SaaS. Atrybucja CC BY 4.0 obowiązkowa.
- **Blokuje kod?** **NIE** (kontrakt HTTP jest w docs). Blokuje **ruch produkcyjny** bez płatnego planu lub self-hostu.
- **Docs:** https://open-meteo.com/en/docs · https://open-meteo.com/en/licence

### - [ ] IMGW / DWD / Météo-France — suplement narodowy

- **Cel:** Opcjonalny feed tenanta obok Open-Meteo, nie jedyne źródło.
- **Co zrobić:** IMGW: publiczny JSON. DWD: Open Data (brak SLA; biznesowy feed TO_VERIFY u `opendata@dwd.de`). Météo-France: rejestracja na portalu API (open data / HVD).
- **Co dostaniemy:** IMGW — bez klucza. DWD — pliki na `opendata.dwd.de`. Météo-France — klucz portalu (TO_VERIFY zakres vs Open-Meteo `v1/meteofrance`).
- **Blokuje kod?** **NIE** (IMGW/DWD). Météo-France: kod vs portal **NIE** po kluczu self-serve.
- **Docs:** https://danepubliczne.imgw.pl/apiinfo · https://www.dwd.de/EN/ourservices/opendata/opendata.html · https://portail-api.meteofrance.fr/web/en/

---

## 2. KSeF

### - [ ] KSeF API 2.0 — wystawianie + zakup (Subject2) **P0**

- **Cel:** Omni jest `ksef_issuer`. Wystawianie FA(3) i zaciąganie FV kosztowych: metadane + XML. Parser XML jest deterministyczny, nie LLM.
- **Co zrobić:** Nic u MF jako „umowa integratora” do startu. Testy na TEST (dane zanonimizowane) albo DEMO (prawdziwe uprawnienia, bez skutków prawnych). Produkcja: token/certyfikat **tenanta**. Limitów więcej: wniosek na stronie integratorów. Kontakt: formularz „Napisz do nas” na portalu podatkowym.
- **Co dostaniemy:** OpenAPI 3.0.4, środowiska TEST / DEMO / PRD, biblioteki referencyjne MF (.NET, Java).
- **Blokuje kod?** **NIE**
- **Docs:** https://ksef.podatki.gov.pl/ksef-na-okres-obligatoryjny/wsparcie-dla-integratorow  
  DEMO: https://api-demo.ksef.mf.gov.pl/docs/v2 · TEST: https://api-test.ksef.mf.gov.pl/docs/v2 · PRD: https://api.ksef.mf.gov.pl/docs/v2  
  Przewodnik: https://github.com/CIRFMF/ksef-docs  
  Potwierdzone w przewodniku MF: `POST /invoices/query/metadata`, `GET /invoices/ksef/{ksefNumber}` (ścieżki względem `/v2`). Pole filtra Subject2 — **TO_VERIFY** w aktualnym OpenAPI (docs pokazują `SubjectType` / `SUBJECT1` w przykładach).

---

## 3. Odpady i monitoring ładunku

### - [ ] BDO REST (KPO / KPOK) **P0**

- **Cel:** Omni nie zastępuje BDO. Wystawia/potwierdza KPO przez API tenanta, numery na `shipment`, HITL przed zapisem.
- **Co zrobić:** Formularz https://bdo.mos.gov.pl/kontakt/ — temat **„integracja z API”**. Infolinia 22 34 04 050 (pn–pt 8–16). API jest **bezpłatne** (IOŚ-PIB). Kontrakt API zmienia się **1.01.2027** — projektować pod nową spec (Excel zmian na stronie BDO).
- **Co dostaniemy:** Klucze integratora + swagger test. GUI: `rejestr-bdo.mos.gov.pl`.
- **Blokuje kod?** **NIE** wobec opublikowanego swaggera. Live/test z kluczami — po formularzu.
- **Docs:** https://bdo.mos.gov.pl/integracja-z-bdo-api/  
  Swagger test: https://test-bdo.mos.gov.pl/api/swagger/index.html  
  Zmiany 2027: https://bdo.mos.gov.pl/news/informacja-dla-integratorow-api-bdo-zmiany-w-ewidencji-odpadow-od-2027-r/

### - [ ] SENT — zgłoszenia (PUESC webservice) **P0**

- **Cel:** Katalog `monitoring_scheme`; P0 zgłoszeń PL. XML zgodny ze spec SENT, nie „SENT-Europa”.
- **Co zrobić:** Specyfikacje z PUESC (kanał DIRECT + XSD). Dostęp niewizualny: mail **`projektsent.ias.zielonagora@mf.gov.pl`** (FAQ PUESC: webservice dla dużej liczby zgłoszeń). Konto PUESC. Alternatywa: formularz w GUI / e-mail `puesc@mf.gov.pl` z XML.
- **Co dostaniemy:** WSDL test/prod, XSD komunikatów. Direct (FAQ/PDF): `https://wstest.puesc.gov.pl/seap_wsChannel_direct/DocumentHandlingPort?wsdl` oraz `https://ws.puesc.gov.pl/seap_wsChannel_direct/DocumentHandlingPort?wsdl`.
- **Blokuje kod?** **NIE** (XSD publiczne). Live webservice — po weryfikacji MF.
- **Docs:** https://puesc.gov.pl/uslugi/uslugi-sieciowe-informacje-i-specyfikacje  
  SENT: https://puesc.gov.pl/uslugi/uslugi-sieciowe-informacje-i-specyfikacje/system-sent  
  FAQ: https://puesc.gov.pl/faq/-/categories/645678496

### - [ ] SENT-GEO — GPS do rejestru (ZSL/OBU)

- **Cel:** Wizja: GPS na czas zgłoszenia. To **interfejs operatora ZSL/OBU** (POST REST-JSON do serwerów SENT-GEO), nie TMS czytający flotę. Omni **nie** staje się operatorem ZSL (zero własnego HW). Pozycja na zleceniu idzie z huba telematycznego; numer biznesowy urządzenia (format `U/Z…`) może trafić na zgłoszenie SENT.
- **Co zrobić:** Nic jako Omni-ZSL. Jeśli tenant/przewoźnik ma ZSL: operator rejestruje ZSL100 na PUESC. Lista operatorów e-TOLL: https://www.gov.pl/web/kas/informacje-dla-operatorow-obu-i-zsl
- **Co dostaniemy:** Nie nasze credentials. Schema: `sgdi_rest_request_schema_v_0_6_1.json` na PUESC/KAS.
- **Blokuje kod?** **NIE** dla flagi SENT + numeru urządzenia z tenanta. **TAK** gdybyśmy chcieli sami pchać GPS do SENT-GEO (poza wizją).
- **Docs:** https://www.gov.pl/web/kas/struktura-interfejsu-sent-geo · instrukcja ZSL na PUESC (system SENT)

### - [ ] EKAER (HU)

- **Cel:** P0 zgłoszeń obok SENT. XML `manageTradeCards` / `queryTradeCards`, nie SOAP/WSDL.
- **Co zrobić:** Spec PDF + XSD z NAV. Test: list do NAV (formularz na FAQ). Prod: `https://import.ekaer.nav.gov.hu/TradeCardManagementService/customer/{OPERATION}` (m.in. `manageTradeCards`).
- **Co dostaniemy:** Spec 2.2 (2025), XSD. Certyfikat/konto — **TO_VERIFY** w PDF NAV (nie zmyślać pól auth).
- **Blokuje kod?** **NIE** (spec publiczna). Sandbox — po liście do NAV.
- **Docs:** https://ekaer.nav.gov.hu/faq/  
  Spec: https://ekaer.nav.gov.hu/faq/content/uploads/2025/05/eKAERManagementService_2.2.pdf

### - [ ] RO e-Transport (UIT)

- **Cel:** P0 zgłoszeń RO. Upload XML + UIT.
- **Co zrobić:** Specyfikacja ANAF/MF RO. Auth: certyfikat cyfrowy albo OAuth2 (oba w PDF). Test: `https://api.anaf.ro/test/ETRANSPORT/ws/v1/upload/{standard}/{cif}` ze `standard=ETRANSP`.
- **Co dostaniemy:** PDF usług; credentials tenanta RO.
- **Blokuje kod?** **NIE** (PDF publiczny). Live — certyfikat/OAuth tenanta.
- **Docs:** https://mfinante.gov.ro/static/10/eTransport/etransport_29072024.pdf

### - [ ] DIWASS (UE odpady transgranica, od 21.05.2026)

- **Cel:** WSR 2024/1157 + IR 2025/1290. GUI albo API oprogramowania komercyjnego. Annex VII papier do 31.12.2026 (KE, marzec 2026).
- **Co zrobić:** Operator musi być zarejestrowany w DIWASS i mieć usera w GUI. **Potem** Helpdesk Komisji o dane API. Dokumentacja API KE: styczeń 2026, update 31 marca — link „here” na stronie Green Forum (fetch nie oddał URL pliku — **TO_VERIFY** dokładny CIRCABC/WSDL). Nie cytować stron trzecich jako kanonu.
- **Co dostaniemy:** TO_VERIFY: WSDL + OAuth client credentials (IR 2025/1290; szczegóły po Helpdesku).
- **Blokuje kod?** **TAK** do oficjalnego pakietu WSDL. Flaga + checklista ręcznego GUI — **NIE**.
- **Docs:** https://green-forum.ec.europa.eu/green-business/digital-waste-shipment-system-diwass_en  
  IR: EUR-Lex 2025/1290

---

## 4. Trans.eu i giełdy

### - [ ] Trans.eu Partners API — scoring / dokumenty **P0**

- **Cel:** Snapshot `overall_rating`, `contractors_satisfaction`, `trans_risk`, `payments_status`, `documents[].expire_date` na `party` z `source_ref`. Próg blokady = dane M-03. Zakaz scrapingu profili.
- **Co zrobić:** Regulamin: wniosek o API → Trans.eu kontaktuje się w 5 dni, może odmówić. Mail **`api@trans.eu`**. Formularz: https://www.trans.eu/api/software-provider-form/ ( treść formularza w fetch = nawigacja docs — **TO_VERIFY** czy to jedyny kanał vs formularz na trans.eu/pl).
- **Co dostaniemy:** `access_token` + unikalny Api-key aplikacji + `client_id`/`client_secret` (nagłówki w docs monitoring).
- **Blokuje kod?** **NIE** wobec opublikowanego JSON. Live — po weryfikacji.
- **Docs:** https://www.trans.eu/api/  
  Partner po id: `GET https://api.platform.trans.eu/ext/partners-api/v1/partners/{UID}`  
  Pola: https://www.trans.eu/api/partners/contractor-description/  
  Regulamin: https://www.trans.eu/api/regulations/

### - [ ] Trans.eu monitoring + trace (per transport) **P0**

- **Cel:** Widoczność **zadania transportowego**, nie całej floty. Okno = `trip.assigned` → grace.
- **Co zrobić:** Te same klucze API co wyżej.
- **Co dostaniemy:**  
  `GET /ext/transports-api/v1/transports/{transport_task_id}/monitoring`  
  `GET /ext/transports-api/api/rest/v1/transports/{transport_id}/trace` (GeoJSON MultiPoint + timestamps)  
  Base: `https://api.platform.trans.eu`
- **Blokuje kod?** **NIE** (docs). Live — klucze.
- **Docs:** https://www.trans.eu/api/transports-in-realization/downloading-information-about-monitoring-events-in-transport-tasks/  
  Trace: https://www.trans.eu/api/transports-in-realization/retrieve-monitoring-trace/

### - [ ] Trans.eu — lista komentarzy słownych + Messenger

- **Cel:** Opinie po transakcji (120 dni) są na platformie. Messenger do negocjacji.
- **Co zrobić:** W publicznym Partners API **nie ma** endpointu listy komentarzy (struktura partnera: rating + satisfaction + risk + documents). **TO_VERIFY** u `api@trans.eu`. Messenger: w spisie metod API (IX 2026) **brak** historii czatu. Zakaz scrapingu. Wolno: oficjalne API/eksport konta tenanta + HITL → `rate_line`.
- **Co dostaniemy:** Póki co nic publicznego do czatu/komentarzy.
- **Blokuje kod?** Snapshot scoringu — **NIE**. Komentarze/czat — **TAK** do oficjalnego endpointu (inaczej nie kodować).
- **Docs:** contractor-description (brak comments[]); nawigacja API: https://www.trans.eu/api/authorization/

### - [ ] TIMOCOM — Shipment Tracking / Tracking API

- **Cel:** Status, ETA, GPS per shipment; ~299 providerów po ich stronie.
- **Co zrobić:** Portal https://developer.timocom.com — **brak self-serve**. Klient TIMOCOM + account manager + OAuth2. API tracking w TMS: billing wg wolumenu (strona usług).
- **Co dostaniemy:** Credentials OAuth2 po akceptacji biznesowej.
- **Blokuje kod?** **TAK** (pełny kontrakt za loginem AM). Stub interfejsu — **NIE**.
- **Docs:** https://www.timocom.co.uk/services/interfaces · https://developer.timocom.com/docs/introduction-1/3h7zifp8eea2m-getting-started

### - [ ] Transporeon — Open Visibility API

- **Cel:** Pozycja + ETA per shipment, geofencing, reguły udostępniania. Czat nie jest produktem integracji TMS.
- **Co zrobić:** Klucz z Visibility Hub. Carrier zaproszony przez klienta: ticket. Shipper: kontakt Transporeon. Guide PDF: Bearer na `https://api.sixfold.com`, m.in. `GET /v1/open-visibility/shipments`.
- **Co dostaniemy:** API key (Bearer).
- **Blokuje kod?** **NIE** wobec PDF v3. Live — klucz Hub.
- **Docs:** https://www.transporeon.com/en/platform/transport-execution-visibility-hub/integrations/open-visibility-data  
  PDF: https://www.transporeon.com/website/pdf/open-visibility-data/open-visibility-api-guide-v3.pdf  
  Portal (konto): https://transporeon-hcskb.atlassian.net/wiki/spaces/ADPD/pages/27233989/Visibility+API

### - [ ] Teleroute (Alpega) — oferty, nie tracking

- **Cel:** CRUD fracht/pojazd. Visibility = osobny produkt Alpega/Wakeo, **nie** T-Interface.
- **Co zrobić:** Konto biznesowe + Integration team. Support: https://teleroute.com/en-en/contact/support/
- **Co dostaniemy:** JWT (`POST /user/token`). Live `https://api.fx.wktransportservices.com`, demo `https://api.fx.demo.wktransportservices.com`. Docs podają `client_id=freightexchange` — **TO_VERIFY** czy to stałe dla wszystkich TMS, czy przykład.
- **Blokuje kod?** **NIE** (docs). Live — konto.
- **Docs:** https://api-docs.teleroute.com/

---

## 5. Hub telematyczny (zero własnego HW)

### - [ ] GBOX (Inelo) **P0**

- **Cel:** Native adapter P0. Credentials z panelu przewoźnika, nie Omni-as-Inelo.
- **Co zrobić:** Inelo BOK **(22) 113 40 60**. Klucze: GBOX Online → Ustawienia → Dostępy (pełna wersja panelu). Docs API: https://docs.gbox.pl/api/doku.php?id=start — fetch 2026-09-07: **„Brak dostępu” / login**.
- **Co dostaniemy:** Dane API Meet GBOX (generowane w panelu). Pełny swagger — po koncie.
- **Blokuje kod?** **TAK** na kompletny klient (docs za loginem). Istnienie API potwierdza FAQ Inelo.
- **Docs:** https://inelo.pl/strefa-qa/kary-e-toll-przepisy/ (wskazuje docs.gbox.pl) · https://online.gbox.pl/pomoc/dostepy.htm

### - [ ] IKOL **P0**

- **Cel:** `iaGetLocatorLastPosition` — ostatnia pozycja lokatora.
- **Co zrobić:** Przewoźnik: user API + hasło lub `sid` + `key` lokatora. Limit w docs: 1 request / lokator / 60 s.
- **Co dostaniemy:** Publiczny kontrakt query: `https://api.ikol.pl/iaGetLocatorLastPosition?...` (`login`, `password`/`sid`, `key`, `output`, `timezone`).
- **Blokuje kod?** **NIE**
- **Docs:** https://ikol.pl/baza-wiedzy/api-ikol/

### - [ ] Flotis REST **P0**

- **Cel:** Firmy / pojazdy / ostatnie pozycje.
- **Co zrobić:** Admin Flotis daje `client-id` + `client-secret` (Basic) oraz `api-key` do pozycji. Docs EN v1.2 (2022-02-01). Endpoint companyId **wyłączony od 2022-06-01** — używać api-key.
- **Co dostaniemy:** `GET /flotis-api/secured/external/positions/api-key/{api-key}` · `Authorization: Basic …` · `Accept: application/vnd.flotis.pl-ext1+json`
- **Blokuje kod?** **NIE**
- **Docs:** https://kontakt.flotis.pl/api/index_en/

### - [ ] Wialon (Gurtam) SDK **P0**

- **Cel:** Remote API — pozycja jednostki. Hosting: zwykle `hst-api.wialon.com`; Local = host tenanta.
- **Co zrobić:** Konto Wialon Hosting/Local tenanta. Token/sesja (`sid`) po `token/login` (szczegóły w docs SDK).
- **Co dostaniemy:** Publiczny kontrakt `https://{host}/wialon/ajax.html?svc=…&params={…}&sid=…`
- **Blokuje kod?** **NIE**
- **Docs:** https://help.wialon.com/en/api/expert-articles/introduction-to-sdk/basic-requests

### - [ ] Teltonika — pakiet Omni (opcjonalny HW)

- **Cel:** Urządzenia u przewoźnika, który chce. Protokół z wiki, **TO_VERIFY per model**.
- **Co zrobić:** Wiki Codec 8 / 8E / 16. Parser toolkit z Universal Device Test Guide. Zakaz własnego firmware.
- **Co dostaniemy:** Specyfikacja binarna (publiczna). Serwer TCP/UDP Omni = osobna decyzja ops (nie aggregator).
- **Blokuje kod?** **NIE** (wiki). Model AVL ID — TO_VERIFY przy SKU.
- **Docs:** https://wiki.teltonika-gps.com/view/Teltonika_Data_Sending_Protocols

### - [ ] Queclink — pakiet Omni (opcjonalny HW)

- **Cel:** Drugi vendor HW. `@track Air Interface` jest w manualach serii (np. GL521M) — PDFy na Scribd/resellerach, **nie** publiczny portal API.
- **Co zrobić:** Kontakt Queclink / dystrybutor o protokół **konkretnego** SKU. Nie zgadywać ramek z wycieków.
- **Co dostaniemy:** PDF protokołu po NDA/partnerstwie — **TO_VERIFY**.
- **Blokuje kod?** **TAK** do oficjalnego PDF modelu.

### - [ ] Linkway INTEGRATOR — aggregator (~230)

- **Cel:** Gdy brak native adaptera. Jeden kontrakt.
- **Co zrobić:** Linkway Sp. z o.o., pl. Andersa 7, 61-894 Poznań. **`biuro@linkway.pl`**, tel. **+48 533 314 921**. Cennik/umowa API TMS — **TO_VERIFY** (strona sprzedaje panel + BRIDGE, nie publiczny swagger Omni).
- **Co dostaniemy:** Umowa + credentials. Publicznego OpenAPI INTEGRATOR-as-TMS **nie ma** na stronie (IX 2026).
- **Blokuje kod?** **TAK**
- **Docs:** https://linkway.pl/tools/linkway-integrator/ · https://linkway.pl/llms.txt

### - [ ] DRIP — aggregator (~400)

- **Cel:** Drugi aggregator. REST + webhooks.
- **Co zrobić:** Partner technologiczny: https://drip-log.com/en/technology-partner/ · sandbox w onboardingu. Support: `support@drip-log.com`.
- **Co dostaniemy:** Docs + swagger `https://ws.drip-log.com/q/swagger/` (help.drip-log.com). Umowa/cennik — **TO_VERIFY**.
- **Blokuje kod?** **NIE** wobec swaggera. Live — onboarding.
- **Docs:** https://help.drip-log.com/de/Interfaces/Working-version/

### - [ ] Webfleet.connect / Geotab (EU, nie P0 PL)

- **Cel:** API potwierdzone publicznie (benchmark). Native gdy tenant BYO.
- **Co zrobić:** Webfleet: wniosek klucza (klient: support portal / integrator: .connect Partner Program) + osobne konto WEBFLEET.connect. Geotab: SDK publiczny; sesja do bazy tenanta.
- **Co dostaniemy:** Webfleet API key. Geotab session token.
- **Blokuje kod?** Webfleet: **NIE** (PDF Reference). Geotab: **NIE**.
- **Docs:** https://www.webfleet.com/en_us/webfleet/partners/integration/developer-resources/  
  Geotab: https://developers.geotab.com/myGeotab/introduction/

### - [ ] Reszta GPS PL (Cartrack, Navifleet, Tronik ATRAX4, Logisat, …)

- **Cel:** Native dopiero po dokumentacji. Do tego czasu aggregator.
- **Co zrobić:** Umowa z vendorami / docs „na życzenie” (Logisat, Tronik — brak publicznego swaggera w weryfikacji).
- **Co dostaniemy:** TO_VERIFY per vendor.
- **Blokuje kod?** **TAK** per vendor bez docs.

---

## 6. Mapy

### - [ ] OpenFreeMap **P0**

- **Cel:** Darmowy podkład wektorowy bez klucza Omni. Atrybucja OSM (+ OpenFreeMap mile widziane). Komercja **dozwolona** (FAQ). Brak SLA.
- **Co zrobić:** Nic. Opcja: sponsor `zsolt@openfreemap.org` / GitHub Sponsors. Self-host PMTiles = admin tenanta.
- **Co dostaniemy:** Public instance, bez API key. Style na openfreemap.org (Positron, Bright, Liberty, Dark, Fiord, 3D). Szablon kafelka — **TO_VERIFY** w ich guide (nie zgadywać URL z pamięci).
- **Blokuje kod?** **NIE**
- **Docs:** https://openfreemap.org/ · https://github.com/hyperknot/openfreemap/

### - [ ] GUGiK Geoportal WMTS (orto + topo PL) **P0**

- **Cel:** Ortofotomapa i mapa topograficzna PL, bez klucza. Dane otwarte.
- **Co zrobić:** Podłączyć WMTS z katalogu GUGiK. GetCapabilities: `?Service=WMTS&Request=GetCapabilities`.
- **Co dostaniemy:** m.in.  
  `https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMTS/StandardResolution`  
  `https://mapy.geoportal.gov.pl/wss/service/PZGIK/ORTO/WMTS/HighResolution`  
  (strona orto GUGiK). Lista wszystkich usług: geoportal „Usługi WMS i WMTS” (URL-e za przyciskiem — kopiować stamtąd, nie zgadywać TOPO).
- **Blokuje kod?** **NIE**
- **Docs:** https://www.geoportal.gov.pl/pl/dane/ortofotomapa-orto/  
  Katalog: https://www.geoportal.gov.pl/pl/usluga/uslugi-przegladania-wms-i-wmts/

### - [ ] OpenTopoMap / CyclOSM / Humanitarian (HOT)

- **Cel:** Darmowe warstwy on/off u użytkownika. Atrybucja OSM + projektu.
- **Co zrobić:** Homepages projektów; ToS kafelków **TO_VERIFY** przy implementacji (fair use). **Zakaz:** `https://tile.openstreetmap.org/{z}/{x}/{y}.png` jako CDN produkcyjny — [polityka OSMF](https://operations.osmfoundation.org/policies/tiles/).
- **Co dostaniemy:** Publiczne kafelki projektów (nie OSMF Standard).
- **Blokuje kod?** **NIE** po potwierdzeniu URL kafelka z homepage.
- **Docs:** OSMF tiles: https://operations.osmfoundation.org/policies/tiles/

### - [ ] Carto Positron / Voyager

- **Cel:** W benchmarku jako darmowe. **Stan 2026:** Carto wymaga klucza nawet na „free basemaps”; limit 5 mln req/mies.; komercja — mogą poprosić o umowę.
- **Co zrobić:** Klucz: https://carto.com/basemaps/apikey/ albo `support-basemaps@carto.com`. Atrybucja OSM + CARTO.
- **Co dostaniemy:** `key=` na `basemaps.cartocdn.com`.
- **Blokuje kod?** **NIE** (self-serve key). Produkcja SaaS — **TO_VERIFY** fair use vs Enterprise.
- **Docs:** https://carto.com/legal/basemap-terms/ · https://carto.com/basemaps/apikey/

### - [ ] Esri World Imagery / World Street

- **Cel:** Opcja darmowa z atrybucją Esri. Limit komercyjny **TO_VERIFY**.
- **Co zrobić:** Atrybucja wg itemu Esri. Nie wklejać klucza ArcGIS Developer, dopóki admin nie wybierze płatnego Esri.
- **Co dostaniemy:** Publiczne basemapy ArcGIS Online (URL kafelka — z itemu Esri, nie zgadywać).
- **Blokuje kod?** **NIE** do wyświetlenia z atrybucją. Produkcja — TO_VERIFY licencji.
- **Docs:** https://support.esri.com/en-us/knowledge-base/what-is-the-correct-way-to-cite-an-arcgis-online-basema-000012040

### - [ ] Płatne podkłady BYO (admin tenanta)

- **Cel:** Katalog `tenant_map_provider` — klucz tenanta, ograniczenie domeny. Omni nie sprzedaje map.
- **Co zrobić:** Tenant sam: Mapbox, MapTiler, Google Maps Platform, HERE, TomTom, PTV Map, Stadia, Thunderforest, Jawg, Azure Maps, Esri ArcGIS, Geoapify, LocationIQ — instrukcja w `podklady-map-admin.md`.
- **Co dostaniemy:** Public token / apiKey tenanta. **Nie** umowa Omni z vendorami.
- **Blokuje kod?** **NIE** (szablon kafelka jako dane).
- **Docs:** konta vendorów jak w `docs/analysis/podklady-map-admin.md` (account.mapbox.com, cloud.maptiler.com, console.cloud.google.com, platform.here.com, developer.tomtom.com, developer.myptv.com, …)

---

## 7. Myto (silnik wyceny, nie EETS)

### - [ ] PTV Developer — Routing + toll

- **Cel:** Geometria + klasa pojazdu + data → `charge` z `source_ref`. Winieta ≠ km.
- **Co zrobić:** Konto https://developer.myptv.com/ — klucz Map/Routing (osobno od podkładu). Cennik wg umowy PTV.
- **Co dostaniemy:** API key. Toll: concept „Toll in Routing” (`getMapInformation` w Data API — czy kraj ma taryfę).
- **Blokuje kod?** **NIE** (docs). Live — klucz.
- **Docs:** https://developer.myptv.com/en/documentation/routing-api/concepts/toll-routing

### - [ ] HERE Routing v8 — truck + `tolls`

- **Cel:** Drugi komercyjny routing+toll. Podkład ≠ licencja floty.
- **Co zrobić:** https://platform.here.com/ — `apiKey`. OpenAPI: `GET https://router.hereapi.com/v8/routes` z parametrami `truck` / `tolls` (w spec OpenAPI).
- **Co dostaniemy:** apiKey. Pokrycie krajów — z docs HERE, nie zgadywać.
- **Blokuje kod?** **NIE**
- **Docs:** https://docs.here.com/routing/docs/routing-v8-intro · OpenAPI: https://router.hereapi.com/v8/openapi

### - [ ] NAPSPAN — routing + opt-in `tolls`

- **Cel:** NAP + truck route; myto jako `include: ["tolls"]`.
- **Co zrobić:** Self-serve klucz (14 dni trial). Kontakt z formularza na napspan.com.
- **Co dostaniemy:** `X-API-Key`. `POST https://api.napspan.com/api/v1/routing/route` (homepage).
- **Blokuje kod?** **NIE**
- **Docs:** https://napspan.com/ · https://napspan.com/blog/toll-cost-routing-api.html

### - [ ] TollCalc

- **Cel:** ~37 krajów HGV. Token Bearer.
- **Co zrobić:** https://tollcalc.eu — `support@tollcalc.eu`. Strona `/en/api.html` w fetch 2026-09-07 prawie pusta — **ścieżki REST TO_VERIFY** na żywej stronie (nie przepisywać z klienta PyPI jako kanonu).
- **Co dostaniemy:** Bearer token. Base w kliencie społecznościowym: `https://app.tollcalc.eu` — **TO_VERIFY** vs oficjalny HTML.
- **Blokuje kod?** **TAK** do potwierdzenia kontraktu na tollcalc.eu/en/api.html. Istnienie produktu — TAK na homepage.
- **Docs:** https://tollcalc.eu/en/api.html · https://tollcalc.eu

### - [ ] Taryfy publiczne (kuracja, nie jeden API UE)

- **Cel:** e-TOLL PL, Toll Collect DE, ASFINAG, HU-GO, SK/CZ, Viapass, LSVA, TollRo — źródła do `source_ref`, nie zmyślona kwota.
- **Co zrobić:** Per urząd — PDF/taryfa. Brak taryfy = warning. EETS (Eurowag, Toll4Europe) **nie** zastępuje silnika TMS.
- **Co dostaniemy:** Tabele/PDF, nie uniwersalny REST.
- **Blokuje kod?** Katalog schem — **NIE**. Precyzyjne kwoty bez PTV/HERE/NAPSPAN — **TAK** per kraj.

---

## 8. ERP / FK

Omni wystawia FV (KSeF = Omni). Adapter nie liczy VAT/marży. Agent outbound. Zakaz SQL `sa` na świat.

### - [ ] Comarch ERP Optima **P0**

- **Cel:** FS przychodowa + FZ kosztowa do Optimy.
- **Co zrobić:** Partner Comarch — **licencja API / WebAPI (SOAP)**. Agent Windows + COM. **Brak** publicznego REST/OpenAPI Comarch (potwierdzają nawet partnerzy; oficjalny REST = nie). Dokumentacja pełna zwykle **za loginem Partnera**.
- **Co dostaniemy:** Licencja + operator API. Nie swagger „dla wszystkich”.
- **Blokuje kod?** **TAK** na kompletny klient COM/SOAP bez kit partnera. Ping agenta — można szkicować po umowie.
- **Docs:** ekosystem Comarch / partner. OCR Comarch to **inny** produkt (`ocr.erp.comarch.pl`) — nie FK.

### - [ ] Comarch ERP XL — CDN API **P0**

- **Cel:** To samo mapowanie FS/FZ przy serwerze XL.
- **Co zrobić:** CDN_API.DLL na hoście XL. Docs: baza XL017 (pomoc.comarch.pl). Licencja integracji **TO_VERIFY** u partnera. REST sklepów partnerskich = nakładka, nie wołać.
- **Co dostaniemy:** Biblioteka + assembly .NET z zasobów XL (Comarch).
- **Blokuje kod?** **TAK** bez CDN_API na maszynie deweloperskiej.
- **Docs:** https://pomoc.comarch.pl/xl/index.php/dokumentacja/xl017-wykorzystanie-api-erp-xl/

### - [ ] Symfonia (Sage / Cegid) WebAPI **P0**

- **Cel:** REST/JSON na instancji tenanta.
- **Co zrobić:** Włączyć WebAPI + klucz aplikacji w panelu. Agent/tunel jeśli tylko LAN. Test: `GET /api/Ping`. Sesja: `GET /api/Sessions/OpenNewSession?deviceName=OmniRoute` z `Authorization: Application {klucz}`, potem `Authorization: Session {guid}`.
- **Co dostaniemy:** Docs 2026 publiczne. Swagger UI opcjonalnie na instancji `/swagger/ui/index`.
- **Blokuje kod?** **NIE** (kontrakt sesji w docs). Live — URL + klucz tenanta.
- **Docs:** https://pomoc.symfonia.pl/data/api/webapi/2026/data/uwierzytelnianie_i_autoryzacja.htm  
  Swagger: https://pomoc.symfonia.pl/data/api/webapi/2026_2/data/swagger_ui.htm

### - [ ] InsERT Subiekt nexo — Sfera **P0**

- **Cel:** Agent przy MSSQL; Sfera w nexo PRO wbudowana, inaczej dokupić. Nie publiczny REST sprzedaży.
- **Co zrobić:** Licencja Sfery / nexo PRO. Portal dewelopera InsERT API (Konto InsERT) dotyczy **aplikacji webowych InsERT** (nexo, Subiekt 123) — **TO_VERIFY** czy to ten sam kanał co Sfera desktop. Nie mylić z REST chmury.
- **Co dostaniemy:** SDK/.NET Sfera lokalnie. Brak publicznego swaggera Sfery.
- **Blokuje kod?** **TAK**
- **Docs:** https://www.insert.com.pl/dla_uzytkownikow/e-pomoc_techniczna/10590,jak-uzyskac-dostep-do-portalu-dewelopera-insert-api-w-serwisie-konto-insert.html

### - [ ] InsERT Subiekt GT — Sfera GT **P0**

- **Cel:** Osobny dodatek „Sfera dla Subiekta GT”. Inny adapter niż nexo.
- **Co zrobić:** Kupić Sferę GT, aktywować bieżącą wersję GT. COM/OLE. Dokumentacja w pakiecie Sfery (nie jeden publiczny REST).
- **Co dostaniemy:** Biblioteka COM `InsERT GT dla aplikacji`.
- **Blokuje kod?** **TAK**
- **Docs:** https://www.insert.com.pl/programy_dla_firm/sprzedaz/sfera_dla_subiekta_gt/opis.html

### - [ ] enova365 WebAPI (P1)

- **Cel:** Kolejny wiersz `erp_connector`. REST + JWT + Swagger **na instancji**. Moduł **licencyjny**.
- **Co zrobić:** Partner enova — moduł WebAPI. Swagger po włączeniu u klienta, nie jeden globalny URL.
- **Co dostaniemy:** JWT + swagger instancji.
- **Blokuje kod?** **TAK** bez modułu/licencji. Kontrakt „REST+JWT+Swagger” — publiczny opis.
- **Docs:** https://enova.pl/moduly-systemu/integracje/webapi/

---

## 9. Poczta Polska — książka nadawcza

### - [ ] Elektroniczny Nadawca — SOAP WebAPI w96 **P0**

- **Cel:** `clearEnvelope` → `addShipment` (max 500) → `getPrintForParcel` → `sendEnvelope` → `getOutboxBook`. `numerNadania` = klucz wiersza. PDF książki = artefakt.
- **Co zrobić:** Rejestracja https://e-nadawca.poczta-polska.pl → **podpisać umowę** → test https://en-testwebapi.poczta-polska.pl → produkcja. GUI zostaje na e-nadawca.poczta-polska.pl. **Nowy** endpoint produkcyjny: `https://e-nadawca.api.poczta-polska.pl/websrv/` (stare `/websrv/` na e-nadawca.poczta-polska.pl do wyłączenia).
- **Co dostaniemy:** Konto EN + WSDL. Spec PDF w96 (17.1.0, 2026-03-18) jest **publiczna**.
- **Blokuje kod?** **NIE** wobec PDF. Live/test z danymi — po umowie.
- **Docs:** https://e-nadawca.poczta-polska.pl/?action=GetAbout (Incapsula może blokować boty — PDF działa)  
  Spec: https://e-nadawca.poczta-polska.pl/download/en_opis_webapi_w96.pdf

### - [ ] Śledzenie REST USS 2.0 **P0**

- **Cel:** Status po `numer_nadania`. Kody zdarzeń (`P_D` Doręczono, `P_UKEPO` podpis), nie nazwy. **Imienia w REST nie ma.** TLS ≥ 1.2 (NIS2/DORA). SOAP `tt.poczta-polska.pl` = zapas.
- **Co zrobić:** Docs publiczne. Demo: login `sledzeniepp`, hasło `PPSA` (hash w docs). Dedykowane konto + `checkmailcollectionex`: **formularz na stronie REST**. `checkmailcollectionex` wymaga uprawnienia.
- **Co dostaniemy:** Token z `login` → nagłówek `api_key`. Prod: `https://uss.poczta-polska.pl` + `/uss/v2.0/tracking/checkmailex` (GET, `number`, `language`).
- **Blokuje kod?** **NIE** (konto demo + spec). Wolumen — formularz.
- **Docs:** https://www.poczta-polska.pl/dla-biznesu/wsparcie/integracje/systemy-sledzenia/system-sledzenia-rest-api/

### - [ ] EPO (`getEPOStatus`) **P0**

- **Cel:** `osobaOdbierajaca` + `podmiotDoreczenia` (ADRESAT, UPOWAZNIONY_PRACOWNIK, …). Usługa na przesyłce: `EPOSimpleType` / `EPOExtendedType`. Papierowe ZPO = skan HITL, nie zgadywanie nazwiska.
- **Co zrobić:** Ta sama umowa EN + zaznaczenie EPO przy nadaniu. Bioepo (`withBioepo`) — nie logować podpisu.
- **Co dostaniemy:** Metoda w tym samym SOAP EN (PDF w96).
- **Blokuje kod?** **NIE** (opis w PDF). Live bez umowy EPO — imię zostaje puste.
- **Docs:** ten sam PDF w96, metoda `getEPOStatus`

---

## 10. Sieci drobnicowe (etykieta obca)

### - [ ] Palletforce Alliance API **P0**

- **Cel:** Etykieta sieci 1:1 (Zebra). **Nie** udawać generatora. Qargo też odsyła do systemu sieci.
- **Co zrobić:** Członkostwo / depot Palletforce. Kontakt: https://www.palletforce.com/en/contact/ · tel. **+44 1283 539392**. E-mail na stronie za Cloudflare — **TO_VERIFY** po otwarciu (nie przepisywać z LinkedIn). Integratorzy (Helm/Voila) wymieniają: Access Key, Customer Account Number, Depot Code — to **nie** jest spec Palletforce; traktować jako wskazówkę, potwierdzić u Palletforce.
- **Co dostaniemy:** Credentials + spec etykiety po umowie. Publicznego developer portalu **brak**.
- **Blokuje kod?** **TAK**. Bez API: własny szablon z polami, które sieć każe na papierze — nie ich kod kreskowy.
- **Docs:** https://www.palletforce.com/en/how-palletforce-technology-transforms-pallet-deliveries/ (API „talk to our team”, bez URL spec)

### - [ ] Palletline / Alliance / inne sieci UK-BE

- **Cel:** Ten sam wzorzec D8: oficjalne API albo plik z ich systemu.
- **Co zrobić:** Depot/członkostwo. Publicznego swaggera Palletline/Alliance **nie znaleziono** (IX 2026). Palletways ≠ Palletforce — nie mylić; Cargoson to warstwa trzecia, nie kanon.
- **Co dostaniemy:** TO_VERIFY per sieć.
- **Blokuje kod?** **TAK**

---

## 11. Skan (ML Kit / VisionKit)

### - [ ] Google ML Kit Document Scanner **P0**

- **Cel:** Android, **on-device** (Play services). FV/cennik: `SCANNER_MODE_BASE_WITH_FILTER` (crop + filtr, bez „wymaż plamy”). POD/ładunek: `FULL` może zjeść pieczątkę — nie na kwocie. Brak zgody kamery w apce (uprawnienie Play services).
- **Co zrobić:** Zależność Maven ML Kit. Nic do Google Cloud. Nie Document AI w chmurze (to BYO, inny produkt).
- **Co dostaniemy:** SDK. Zero tokenu tenanta.
- **Blokuje kod?** **NIE**
- **Docs:** https://developers.google.com/ml-kit/vision/doc-scanner  
  Opcje: https://developers.google.com/android/reference/com/google/mlkit/vision/documentscanner/GmsDocumentScannerOptions

### - [ ] Apple VisionKit — `VNDocumentCameraViewController`

- **Cel:** Systemowy skaner iOS (ten sam pipeline co ML Kit po stronie pliku).
- **Co zrobić:** Framework VisionKit. Dokumentacja Apple (strona wymaga JS; kanoniczny URL poniżej).
- **Co dostaniemy:** System UI. Brak chmury Apple do skanu.
- **Blokuje kod?** **NIE**
- **Docs:** https://developer.apple.com/documentation/visionkit/vndocumentcameraviewcontroller

---

## Co świadomie nie jest na tej liście

| Temat | Dlaczego |
|---|---|
| Lejek oferty (piksel / PDF token) | Własny hosting + Graph; brak vendor API do „zdobycia”. Piksel = zgoda, nie Mailchimp. |
| OpenCV enhance | Biblioteka, nie API. |
| `tile.openstreetmap.org` | Odrzucone (OSMF). |
| Scraping czatów Trans.eu / TIMOCOM / PP śledzenia w HTML | Zakaz (ToS + prawo). |
| Kanały armatorskie live | PARK — poza tą wizją-listą. |

---

## Źródła w repo (zweryfikowane, nie skopiowane ślepo)

- `docs/analysis/benchmark-tms-2026.md` §13g–13p  
- `docs/_knowledge/market/006` … `011`  
- `docs/analysis/erp-fk-adapter.md`  
- `docs/analysis/podklady-map-admin.md`
