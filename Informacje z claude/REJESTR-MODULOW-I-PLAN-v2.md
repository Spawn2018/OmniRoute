# Rejestr modułów i plan budowy v2

Kompletna inwentaryzacja wszystkiego, co zaprojektowaliśmy w szesnastu aneksach.
**41 modułów, ~130 obiektów danych.** Każdy moduł: kod, obiekty, funkcje kluczowe,
źródło specyfikacji, przypisane repozytoria.

Kod modułu (`M-xx`) jest identyfikatorem używanym w planie i w `docs/spec/`.

---

# DOMENA A — FUNDAMENT

## M-01 · Wielodostępność
**Spec:** `tenancy.md` ← SPEC-master A5, Rewizja 1.4

| Obiekty | Funkcje kluczowe |
|---|---|
| `organization` · `app_user` · `role` · `user_role` · `audit_log` · `usage_metric` | RLS na poziomie bazy · kontekst tenanta w sesji · audyt triggerem · metering od dnia 1 · routing do bazy dedykowanej |

**Repozytoria:** `supabase/supabase` (wzorzec RLS) · `citusdata/citus` · `postgresml/pgcat` · `openfga/openfga` · `casbin/casbin` · `kvesteri/sqlalchemy-continuum`

**Reguła architektoniczna:** żadne zapytanie nie sięga po dane więcej niż jednego tenanta. Test w `import-linter` + test integracyjny.

## M-02 · Niezawodność zdarzeń
**Spec:** `tenancy.md` ← Rewizja 1.5

| Obiekty | Funkcje kluczowe |
|---|---|
| `outbox` · `idempotency_key` · `event_log` | zapis zdarzenia w transakcji ze zmianą stanu · publikacja osobnym procesem · klucz idempotencji na każdym wywołaniu zewnętrznym · odtwarzanie strumienia |

**Repozytoria:** `tembo-io/pgmq` · `temporalio/temporal` · `dbos-inc/dbos-transact-py`

## M-03 · Konfiguracja per organizacja
**Spec:** `tenancy.md` ← SPEC-master B10

| Obiekty | Funkcje kluczowe |
|---|---|
| `document_template` · `numbering_scheme` · `workflow_definition` · `margin_rule` · `custom_field` · `currency_display_rule` · `quote_automation_policy` · `rate_gap_policy` · `auto_quote_policy` | numeracja transakcyjna bez dziur · szablony per tenant · workflow konfigurowalny · pola własne |

**Repozytoria:** `frappe/frappe` (wzorzec metadanowy) · `flipt-io/flipt` · `Unleash/unleash` · `open-feature/spec`

## M-04 · Uprawnienia i tożsamość
**Spec:** `tenancy.md`

| Obiekty | Funkcje kluczowe |
|---|---|
| model relacyjny OpenFGA · `screening_whitelist` (uprawnienia zwolnień) | „handlowiec widzi swoich klientów" · zasada dwóch par oczu powyżej progu · SSO korporacyjne |

**Repozytoria:** `openfga/openfga` · `keycloak/keycloak` · `ory/kratos` · `logto-io/logto` · `authelia/authelia`

---

# DOMENA B — DANE REFERENCYJNE

## M-05 · Geografia
**Spec:** `reference.md` ← Aneks 13 §4, Aneks 1 §3.1

| Obiekty | Funkcje kluczowe |
|---|---|
| `port` (UN/LOCODE) · `terminal` · `location` (unlocode\|postal_zone\|address\|terminal) · `location_zone_member` | normalizacja aliasów portów · strefy taryfowe per organizacja · kody ISPS · charakterystyka portu z World Port Index |

**Repozytoria:** `cristan/improved-un-locodes` ← podstawa · `datasets/un-locode` · `geoapify/un-locode` · `marek5050/UN-LOCODE` · `tadziqusky/unlocode-ports` · `SeaconLogistics/un_locode` · `dr5hn/countries-states-cities-database` · `mledoze/countries`

## M-06 · Słownik opłat
**Spec:** `charges.md` ← SPEC-master B4

| Obiekty | Funkcje kluczowe |
|---|---|
| `charge_code` (~60 kodów, 5 grup) · `charge_code_alias` (wielojęzyczny) · `incoterm` · `container_type` | mapowanie alias → fuzzy → embedding · uczenie z korekt · aliasy per kontrahent · wymagalność per incoterm |

**Repozytoria:** `rapidfuzz/RapidFuzz` · `seatgeek/thefuzz` · `pgvector/pgvector` · `FlagOpen/FlagEmbedding` (polszczyzna) · `dedupeio/dedupe`

## M-07 · Waluty i czas
**Spec:** `finance.md` §1 ← Aneks 16

| Obiekty | Funkcje kluczowe |
|---|---|
| `fx_rate` (NBP tabela A, historia) · `datasets/currency-codes` | kurs D-1 roboczy · trzy kursy: podatkowy, zarządczy, faktyczny · typ `Money` · zaokrąglanie per waluta |

**Repozytoria:** `limist/py-moneyed` · `python-babel/babel` · `sdispater/pendulum` · `dinerojs/dinero.js` · `fawazahmed0/exchange-api` · `datasets/currency-codes`

## M-08 · Towary niebezpieczne
**Spec:** `compliance.md` ← Aneks 13 §5

| Obiekty | Funkcje kluczowe |
|---|---|
| `dg_substance` · `dg_segregation_rule` · `shipment_dg_item` · `carrier_dg_acceptance` | walidacja kombinacji UN/klasa/grupa · segregacja w kontenerze · akceptacja przez armatora · cut-off DG · limited quantity |

**Uwaga prawna:** tekst IMDG i IATA DGR chroniony. Buduj z publicznych załączników ADR. System waliduje, nie klasyfikuje.

## M-09 · Kody towarowe
**Spec:** `reference.md`

| Obiekty | Funkcje |
|---|---|
| `hs_code` · powiązanie z listą podwójnego zastosowania | podpowiadanie HS z opisu · sygnalizacja kontroli eksportu |

**Repozytoria:** `datasets/harmonized-system`

---

# DOMENA C — KONTRAHENCI

## M-10 · Kontrahenci
**Spec:** `parties.md` ← SPEC-master B2

| Obiekty | Funkcje kluczowe |
|---|---|
| `party` (role tablicą) · `party_contact` · `party_bank_account` · `party_charge_override` · `party_email_domain` · `carrier_profile` | jeden podmiot w wielu rolach · autouzupełnianie po NIP · weryfikacja rachunku · preferencje walutowe |

**Repozytoria:** `bigzbig/regonapi` (sandbox bez klucza) · `grzesieksw/GusApi` · `infirsoft/vat-whitelist-api` · `m4rcelpl/WykazPodatnikow` · `twentyhq/twenty` (model danych) · `frappe/erpnext` (wzorzec Party)

## M-11 · Automatyczne kontakty
**Spec:** `parties.md` ← Aneks 10 §3

| Obiekty | Funkcje kluczowe |
|---|---|
| `contact_suggestion` | dopasowanie po domenie · kontekst wątku · ekstrakcja podpisu · kolejka weryfikacji · **wykrywanie podobnych domen jako ostrzeżenie** · retencja RODO |

**Repozytoria:** `SpamScope/mail-parser` · `567-labs/instructor` · `RapidFuzz` · `microsoft/presidio`

## M-12 · Sieci i stowarzyszenia
**Spec:** `parties.md` ← Aneks 8

| Obiekty | Funkcje kluczowe |
|---|---|
| `network` · `network_membership` · `network_member` (per tenant!) · `network_member_contact` · `network_member_link` | import własnego eksportu · deduplikacja między sieciami · wzbogacanie z historii · ranking wg karty wyników · mapa pokrycia agencyjnego |

**Repozytoria:** `dedupeio/dedupe` · `rapidfuzz/RapidFuzz` · pipeline ekstrakcji z M-20

## M-13 · Karta wyników kontrahenta
**Spec:** `parties.md` ← Aneks 4 §2.2

| Obiekty | Funkcje kluczowe |
|---|---|
| `party_scorecard` | wskaźnik odpowiedzi · mediana czasu · pozycja cenowa per relacja · zgodność oferty z fakturą · rollover · kierowanie zapytań do najlepszych |

## M-14 · Ocena kredytowa i wywiadownie
**Spec:** `credit.md` ← Aneks 7

| Obiekty | Funkcje kluczowe |
|---|---|
| `external_data_credential` · `credit_check_authorization` · `credit_report` · `financial_statement` · `financial_ratio` · `credit_assessment` · `credit_watch` · `credit_alert` | KRS API · **RDF: sprawozdania w XML, darmowe** · KRZ · MSiG · CEIDG · scoring deterministyczny · formuła limitu · monitoring zmian · upoważnienie dla JDG |

**Repozytoria:** `bigzbig/regonapi` · KRS openApi · RDF · `infirsoft/vat-whitelist-api`

## M-15 · Wirtualny Dyrektor Finansowy
**Spec:** `credit.md` ← Aneks 7 §2

| Obiekty | Funkcje kluczowe |
|---|---|
| `credit_opinion` · `scoring_model_config` | silnik punktowy (30% waga: własna historia płatnicza) · formuła limitu · sugerowany termin powiązany z kosztem kapitału · notatka generowana przez model · **decyzja zawsze przez człowieka (RODO art. 22)** |

**Repozytoria:** `567-labs/instructor` · `dottxt-ai/outlines` · `guardrails-ai/guardrails`

## M-16 · Procedury operacyjne klienta
**Spec:** `parties.md` ← Aneks 5 §6

| Obiekty | Funkcje |
|---|---|
| `customer_sop` | reguły generujące zadania · walidacje przy zleceniu · wersjonowanie i zatwierdzanie |

---

# DOMENA D — STAWKI ZAKUPOWE

## M-17 · Stawki statyczne
**Spec:** `rates-sheets.md` ← SPEC-master B5, Aneks 1 §3.2, Aneks 14 §1.2

| Obiekty | Funkcje kluczowe |
|---|---|
| `rate_sheet` · `rate_line` (+`validity_basis`, `bracket_unit/from/to`, `origin_context`) · `extraction_template` | niemutowalność · `superseded_by` · przedziały wagowe i LDM · **podstawa ważności: sailing\|booking\|bl_date\|gate_in** · wykrywanie kolizji · świeżość |

**Repozytoria:** `pgvector/pgvector` · `pola-rs/polars` · `great-expectations/great_expectations`

## M-18 · Opłaty portowe warunkowe
**Spec:** `port-charges.md` ← Aneks 15 §1

| Obiekty | Funkcje kluczowe |
|---|---|
| `port_charge_rule` (11 wymiarów warunkowych) | **`is_applicable=false` — wiedza negatywna** · rozstrzyganie przez specyficzność · **uczenie z faktur** · priorytet zaufania: faktura > API > taryfa > oferta |

## M-19 · Stawki live i kanały
**Spec:** `rates-live.md` ← SPEC-master B6, Aneks 12 §2, Aneks 14 §2/§4

| Obiekty | Funkcje kluczowe |
|---|---|
| `carrier_credential` · `carrier_channel` (api\|aggregator\|email\|portal) · `carrier_service` · `carrier_dg_acceptance` · `live_offer` · `live_offer_charge` | **framework adapterów: nowy armator = konfiguracja, nie kod** · brak ważności, TTL · `price_id` do bookingu · wymogi UI armatora · limity i cache per tenant · degradacja przy awarii |

**Repozytoria:** `pact-foundation/pact-python` (testy kontraktowe) · `browser-use/browser-use` · `Skyvern-AI/skyvern` · `steel-dev/steel-browser` · `wiremock/wiremock`

## M-20 · Pipeline ekstrakcji
**Spec:** `extraction.md` ← SPEC-master C2

| Obiekty | Funkcje kluczowe |
|---|---|
| `inbound_message` · `extraction_run` · `review_queue_item` · `classification_feedback` | 9 etapów: ingest→classify→template→layout→extract→normalize→validate→review→commit · `source_ref` obowiązkowe · `unparsed_regions` · pamięć szablonów · uczenie aliasów · wykrywanie anomalii jednostek |

**Repozytoria:** `docling-project/docling` · `datalab-to/marker` · `Unstructured-IO/unstructured` · `microsoft/markitdown` · `jsvine/pdfplumber` · `pymupdf/PyMuPDF` · `camelot-dev/camelot` · `opendataloader-project/opendataloader-pdf` · `tafia/calamine` · `datalab-to/surya` · `PaddlePaddle/PaddleOCR` · `opendatalab/MinerU` · `allenai/olmocr` · `getomni-ai/zerox` · `microsoft/table-transformer` · `567-labs/instructor` · `dottxt-ai/outlines` · `protectai/llm-guard` · `microsoft/presidio` · `langfuse/langfuse` · `promptfoo/promptfoo` · `HumanSignal/label-studio` · `confident-ai/deepeval`
---

# DOMENA E — WYCENA

## M-21 · Silnik wyceny
**Spec:** `quotation.md` ← SPEC-master C4, Aneks 14 §1, Rewizja 1.1

| Obiekty | Funkcje kluczowe |
|---|---|
| `quotation` · `quotation_cargo` · `quotation_variant` · `quotation_line` · `quotation_gap` | **realizacja w SQL, nie w Pythonie** · dobór na `latest_gate_cutoff` (nie ETD) · cut-off DG osobno · równoległe kanały ze strumieniowaniem SSE · wykrywanie luk · liczenie wstecz od ETA · degradacja przy awarii kanału |

**Repozytoria:** `duckdb/duckdb` (analityka) · `tobymao/sqlglot` (walidacja SQL) · Postgres: indeksy pokrywające, widoki materializowane

**Budżet:** p95 < 300 ms ze stawek w bazie, pierwszy wynik < 1 s z kanałami.

## M-22 · Narzuty i marża
**Spec:** `charges.md` ← Aneks 12 §3

| Obiekty | Funkcje kluczowe |
|---|---|
| `markup_rule` (7 poziomów kaskady) | narzut vs marża pokazywane razem · zakres: all_in\|charge_code\|kategoria\|strona\|mode · metody: percent\|fixed\|per_unit\|target_margin\|fixed_sell · **`buy_source: customer_contract`** (kontrakt frachtowy klienta, zerowy narzut) · tryby prezentacji: visible\|folded\|hidden · widoczność zadziałanej reguły · próg minimalnej marży · ostrzeżenie o odchyleniu od mediany |

## M-23 · Waluty w ofercie
**Spec:** `finance.md` §2 ← Aneks 16 §1

| Obiekty | Funkcje kluczowe |
|---|---|
| pola na `quotation`: `currency_mode`, `display_currency`, `fx_clause`, `fx_spread_pct` · `currency_display_rule` | tryby original\|converted\|hybrid · klauzula walutowa generowana do PDF · **spread jako pozycja przychodu** · kurs i data przy każdej pozycji |

## M-24 · Ryzyko oferty
**Spec:** `quotation.md` ← Aneks 4 §2.3–2.4, Aneks 16 §2.5

| Obiekty | Funkcje kluczowe |
|---|---|
| `lane_risk_score` · `quotation_risk` | stawka jako obiekt probabilistyczny (pochodzenie, świeżość, wiarygodność, zmienność) · marża zagrożona · **optymalna ważność oferty** · ekspozycja walutowa netto · GRI ogłoszony przed wypłynięciem |

## M-25 · Negocjacja i wynik
**Spec:** `quotation.md` ← Aneks 3 §2.1, Aneks 4

| Obiekty | Funkcje kluczowe |
|---|---|
| `quotation_negotiation` · `quotation_outcome` | historia negocjacji · próg minimalnej marży z ostrzeżeniem · powód przegranej · cena konkurencji · **krzywa elastyczności cenowej per klient i relacja** · zasilanie `margin_rule` |

## M-26 · Dokument oferty
**Spec:** `quotation.md`

| Obiekty | Funkcje |
|---|---|
| `document_template` (M-03) | dwa układy: rozbity i all-in · wielojęzyczność · klauzula walutowa · „dlaczego ta cena" jednym kliknięciem |

**Repozytoria:** `typst/typst` · `Kozea/WeasyPrint` · `open-xml-templating/docxtemplater` · `MatthiasValvekens/pyHanko` · `Stirling-Tools/Stirling-PDF`

## M-27 · Wycena wsadowa i pokrycie
**Spec:** `quotation.md` ← Aneks 3 §2.1

| Obiekty | Funkcje |
|---|---|
| `rate_coverage_map` (widok) | pięć relacji w jednym zapytaniu · mapa pokrycia stawek: gdzie mam, gdzie wygasło, gdzie biała plama · zestawienie z liczbą zapytań klientów |

---

# DOMENA F — ZAPYTANIA

## M-28 · Zapytania od klientów
**Spec:** `rfq.md` ← Aneks 11

| Obiekty | Funkcje kluczowe |
|---|---|
| `rfq` · `rfq_clarification` · `lead` · `inbound_message` | filtr po domenach klientów · **klasyfikator wieloklasowy (8 klas)** · progi pewności · skrzynka propozycji · wiele relacji w mailu · załączniki jako źródło · **parsowanie dat: zakres + precyzja** · duplikaty · leady z KRS · notatka głosowa |

**Repozytoria:** `SYSTRAN/faster-whisper` · `openai/whisper` · `567-labs/instructor` · `promptfoo/promptfoo`

## M-29 · Wykrywanie akceptacji oferty
**Spec:** `rfq.md` ← Aneks 11 §3

| Obiekty | Funkcje |
|---|---|
| klasa w `inbound_message` | „ok, proszę bookować" w piątek o 16:50 nie ginie · alert · przygotowanie bookingu |

**Priorytet:** najdroższa pojedyncza pomyłka operacyjna. Zrób wcześnie.

## M-30 · Zapytania do agentów i armatorów
**Spec:** `rfq.md` ← Aneks 9, Rewizja 1.2

| Obiekty | Funkcje kluczowe |
|---|---|
| `rate_request` · `rate_request_recipient` | **workflow trwały (Temporal), nie cron** · okno wyboru z rankingiem · personalizacja czterowarstwowa · wysyłka indywidualna · **token per odbiorca** · kaskada 4 poziomów dopasowania odpowiedzi · przypomnienia · okna czasowe stref · uprzedzanie wygasających stawek |

**Repozytoria:** `temporalio/temporal` · `temporalio/sdk-python` · `hatchet-dev/hatchet` · `postalsys/emailengine`

## M-31 · Porównanie odpowiedzi
**Spec:** `rfq.md` ← Aneks 9 §7

| Obiekty | Funkcje |
|---|---|
| widok porównawczy | normalizacja do wspólnych kodów opłat · **wykrywanie braków ważniejsze niż suma** · zapis odpowiedzi jako `rate_line` |

---

# DOMENA G — POCZTA

## M-32 · Integracja pocztowa
**Spec:** `email.md` ← Aneks 10

| Obiekty | Funkcje kluczowe |
|---|---|
| `mailbox_connection` · `email_thread` | **wysyłka z firmowej skrzynki użytkownika** (Graph/Gmail/SMTP) · odczyt tylko własnych wątków po `conversationId` · dedykowany folder · kopia w „Wysłanych" · podpis użytkownika · limity dostawcy · skrzynka zespołowa na urlopy |

**Repozytoria:** `postalsys/emailengine` · `microsoftgraph/msgraph-sdk-python` · `ikvk/imap_tools` · `SpamScope/mail-parser` · `axllent/mailpit` · `docker-mailserver/docker-mailserver`

## M-33 · Dodatek do Outlooka
**Spec:** `email.md` ← Aneks 10 §2.3

| Funkcje |
|---|
| „zarejestruj jako zapytanie" · „dołącz do zlecenia" · panel boczny z limitem kredytowym i otwartymi zleceniami kontrahenta |

## M-34 · Powiadomienia
**Spec:** `notifications.md`

| Obiekty | Funkcje |
|---|---|
| `notification_rule` · `notification_log` | **push z akceptacją jednym dotknięciem** · mail, SMS, in-app · alerty wygasających stawek, ETA, limitu kredytowego, demurrage |

**Repozytoria:** `novuhq/novu` · `caronc/apprise` · `knadh/listmonk` · `postalserver/postal`

---

# DOMENA H — ZLECENIA I TRACKING

## M-35 · Zlecenie
**Spec:** `shipment.md` ← SPEC-master B8, Aneks 1 §3.3

| Obiekty | Funkcje kluczowe |
|---|---|
| `shipment` (+`transport_mode`) · `shipment_sea` · `shipment_road` · `shipment_container` · `shipment_charge` · `shipment_task` · `shipment_document` | konwersja z oferty z zamrożeniem kwot i kursu · maszyna stanów · zadania z SOP · komplet dokumentów z blokadą zamknięcia |

**Repozytoria:** `pytransitions/transitions` · `temporalio/temporal`

## M-36 · Tracking
**Spec:** `tracking.md` ← SPEC-master C5

| Obiekty | Funkcje kluczowe |
|---|---|
| `shipment_event` (model DCSA) · `tracking_subscription` | normalizacja na DCSA niezależnie od formatu armatora · 5 faz cyklu życia · publiczny link dla klienta |

**Repozytoria:** `maplibre/maplibre-gl-js` · `Leaflet/Leaflet` · `visgl/deck.gl`

## M-37 · Zarządzanie wyjątkami
**Spec:** `tracking.md` ← Aneks 3 §2.4

| Obiekty | Funkcje kluczowe |
|---|---|
| `exception_rule` · `exception_event` | rollover · poślizg ETA · **watchdog free time** · cut-off VGM bez zgłoszenia · kontener stoi > X dni · zmiana portu przeładunku · powiadomienie do klienta |

**Priorytet:** najszybszy zwrot w całym systemie.

## M-38 · Dokumenty zlecenia
**Spec:** `documents.md` ← Aneks 3 §2.5

| Funkcje |
|---|
| **walidacja krzyżowa** B/L ↔ booking ↔ VGM ↔ faktura · pętla zatwierdzenia draft B/L przez klienta · lista wymaganych per typ zlecenia · podpis PAdES |

## M-39 · EDI
**Spec:** `edi.md`

| Funkcje |
|---|
| IFTMIN (zlecenie) · IFTSTA (status) · AS2 |

**Repozytoria:** `parcelLab/edi-iftmin` · `xoscar/EDI-IFTMIN` · `nerdocs/pydifact` · `xlate/staedi` · `smooks/smooks` · `OpenAS2/OpenAs2App` · `phax/as2-lib` · `michaelachrisco/Electronic-Interchange-Github-Resources`
---

# DOMENA I — FINANSE

## M-40 · Fakturowanie i KSeF
**Spec:** `finance.md` §3

| Obiekty | Funkcje |
|---|---|
| `invoice` · `invoice_line` · `bill` · `credit_note` · `debit_note` · `payment` | KSeF 2.0: sesje, szyfrowanie, XAdES, QR · wizualizacja XML→PDF · FA(3) · JPK |

**Repozytoria:** `CIRFMF/ksef-api` · `smekcio/ksef-client-python` · `ArturSkowronski/ksef-cli` · `m32/ksef` · `m32/ksef-pdf` · `Pafkaja/ksef_faktury_list` · `fakturownia/API` · `akretion/factur-x` · `phax/ph-ubl`

## M-41 · Rozliczenie wyceny z fakturą
**Spec:** `finance.md` ← Aneks 4 §2.1

| Obiekty | Funkcje kluczowe |
|---|---|
| `cost_variance` | porównanie pozycja po pozycji · typ rozbieżności · spór i odzysk · **zapisywanie reguł opłat portowych z faktur (M-18)** · raport miesięczny |

**Najmocniejsza pojedyncza funkcja w systemie.**

## M-42 · Bank i dopasowanie płatności
**Spec:** `finance.md`

| Obiekty | Funkcje |
|---|---|
| `bank_statement` · `bank_transaction` · `payment_match` | **MT940** · PSD2 · automatyczne dopasowanie do faktur · kompensata rozrachunków |

**Repozytoria:** `WoLpH/mt940` · `nordigen/nordigen-python` · `csingley/ofxtools` · `beancount/smart_importer` (wzorzec dopasowania)

## M-43 · Koszt pieniądza
**Spec:** `finance.md` ← Aneks 6

| Obiekty | Funkcje kluczowe |
|---|---|
| `cost_of_capital_config` · `payment_term_profile` · `shipment_cash_event` · `shipment_financing` · `party_payment_behavior` | **`FINCOST` jako pozycja `shipment_charge`** · terminy rzeczywiste vs umowne (DSO/DPO) · symulacja terminu jako dźwigni handlowej · negocjacja z dostawcami wyrażona kwotą |

## M-44 · Różnice kursowe
**Spec:** `finance.md` ← Aneks 16 §2

| Obiekty | Funkcje kluczowe |
|---|---|
| `shipment_fx_result` · rozszerzenia `shipment_cash_event` | **`FXDIFF` jako pozycja `shipment_charge`** · zrealizowane i niezrealizowane · **ekspozycja netto per zlecenie pokazywana przy wycenie** · zmienność z własnej historii |

## M-45 · Przepływy i ekspozycja portfela
**Spec:** `finance.md` ← Aneks 6 §2, Aneks 5 §4

| Obiekty | Funkcje |
|---|---|
| `cash_flow_forecast` (widok) · `fx_exposure` (widok) · `deposit` | prognoza kasowa z otwartych zleceń · ekspozycja walutowa w oknach czasowych · decyzja o faktoringu per faktura · kaucje i gwarancje z alertem zwrotu |

## M-46 · Koszt obsługi klienta
**Spec:** `finance.md` ← Aneks 5 §5

| Obiekty | Funkcje |
|---|---|
| `cost_to_serve` · `user_activity_log` | minuty operatora · maile · korekty dokumentów · wyjątki · **trójwymiarowa rentowność: brutto / po obsłudze / po kapitale** |

## M-47 · Księgowość — integracja
**Spec:** `finance.md`

| Funkcje |
|---|
| eksport do systemu księgowego · plan kont · warstwa abstrakcji nad dostawcą |

**Repozytoria:** `beancount/beancount` (model do przeczytania) · `tigerbeetle/tigerbeetle` (wzorzec wymuszania reguł przez bazę) · `fakturownia/API`

---

# DOMENA J — GAŁĘZIE TRANSPORTU

## M-48 · Transport drogowy
**Spec:** `road.md` ← Aneks 1

| Obiekty | Funkcje kluczowe |
|---|---|
| `tour` · `tour_assignment` · `shipment_road` | **silnik alokacji: shared / capacity / marginal** · koszt krańcowy doładunku · puste powroty · alokacja → `shipment_charge` · pętla zwrotna do `margin_rule` |

**Repozytoria:** `google/or-tools` · `skjolber/3d-bin-container-packing` · `jerry800416/3D-bin-packing` · `PyVRP/PyVRP` · `TimefoldAI/timefold-solver` · `coin-or/pulp` · `Project-OSRM/osrm-backend` · `valhalla/valhalla` · `graphhopper/graphhopper`

## M-49 · Kolej intermodalna
**Spec:** `rail.md` ← Aneks 14 §3, Aneks 15 §3

| Obiekty | Funkcje kluczowe |
|---|---|
| `rail_operator` · `rail_service` · `rail_rate` · `rail_booking` | terminal-do-terminalu · rozkłady stałe · **porównanie droga/kolej z emisją CO₂** · RID · reefer na kolei · kanał mailowy |

## M-50 · Kolej z Chin
**Spec:** `rail.md` ← Aneks 15 §4

| Obiekty | Funkcje kluczowe |
|---|---|
| rozszerzenia `rail_service`: `corridor`, `gauge_change_point`, `transit_countries` · `route_sanctions_check` | **sprawdzanie trasy wobec list sankcyjnych, nie tylko stron** · przeładunek na inny rozstaw jako osobna pozycja · porównanie morze/kolej/lot w jednej ofercie · LCL kolejowy |

## M-51 · Drobnica morska
**Spec:** `lcl.md` ← Aneks 15 §5

| Obiekty | Funkcje kluczowe |
|---|---|
| `lcl_rate` · `consolidation` · `consolidation_item` | **waga obliczeniowa W/M liczona kodem** · minimum · cut-off CFS wcześniejszy · **próg opłacalności LCL vs FCL** · konsolidatorzy jako dostawcy |

## M-52 · Ślad węglowy
**Spec:** `esg.md` ← Aneks 5

| Obiekty | Funkcje |
|---|---|
| `emission_factor` · `shipment_emissions` | GLEC / ISO 14083 · emisja per przesyłka i per gałąź · zasilanie porównania gałęzi · raport dla klienta objętego CSRD |

---

# DOMENA K — ZGODNOŚĆ

## M-53 · Sankcje
**Spec:** `compliance.md` ← Aneks 13 §3

| Obiekty | Funkcje kluczowe |
|---|---|
| `sanctions_list` · `sanctions_entry` · `screening_run` · `screening_hit` · `screening_whitelist` | pobieranie codzienne UE/ONZ/OFAC/OFSI · **przeskanowanie wszystkich przy zmianie listy** · transliteracja · **screening statków po IMO** · kraje tranzytu · `list_versions` jako wymóg audytowy |

## M-54 · Ochrona przed oszustwem
**Spec:** `compliance.md` ← Aneks 5 §7

| Obiekty | Funkcje |
|---|---|
| `bank_change_request` · `domain_similarity_alert` | zmiana rachunku wymaga potwierdzenia innym kanałem · wykrywanie podobnych domen · próg z dwiema parami oczu · alert przy pierwszej płatności na nowy rachunek |

## M-55 · Reklamacje
**Spec:** `claims.md` ← Aneks 5 §3

| Obiekty | Funkcje |
|---|---|
| `claim` · `claim_document` | terminy zawite liczone automatycznie · korespondencja z ubezpieczycielem · powiązanie ze zleceniem |

## M-56 · RODO i audyt
**Spec:** `compliance.md`

| Obiekty | Funkcje |
|---|---|
| `processing_record` · `retention_policy` · `data_export_request` | rejestr czynności · retencja z automatycznym usuwaniem · eksport danych tenanta · przełącznik przetwarzania lokalnego |

**Repozytoria:** `microsoft/presidio` · `protectai/llm-guard` · `pyca/cryptography`

---

# DOMENA L — WARSTWA AI I ANALITYKA

## M-57 · Serwer MCP
**Spec:** `ai.md` ← Aneks 4 §D1.1

| Funkcje |
|---|
| narzędzia odczytowe bez ograniczeń · zapisowe w trybie „przygotuj do zatwierdzenia" · `search_rates`, `create_quotation`, `get_shipment_status`, `list_expiring_rates`, `explain_charge` |

**Repozytoria:** `modelcontextprotocol/python-sdk` · `modelcontextprotocol/inspector` · `modelcontextprotocol/servers` · `wong2/awesome-mcp-servers`

## M-58 · Copilot w interfejsie
**Spec:** `ai.md`

| Funkcje |
|---|
| zdanie → wypełniony formularz · funkcja demonstracyjna |

**Repozytoria:** `CopilotKit/CopilotKit` · `vercel/ai` · `assistant-ui/assistant-ui`

## M-59 · Raporty językiem naturalnym
**Spec:** `ai.md` ← Aneks 4 §D1.3

| Obiekty | Funkcje |
|---|---|
| warstwa semantyczna | text-to-SQL przeciwko warstwie semantycznej · **walidacja SQL obowiązkowa** · replika do odczytu |

**Repozytoria:** `Canner/WrenAI` · `cube-js/cube` · `tobymao/sqlglot` · `vanna-ai/vanna` · `duckdb/duckdb` · `metabase/metabase`

## M-60 · Cyfrowi współpracownicy
**Spec:** `ai.md` ← Aneks 4 §2.7

| Obiekty | Funkcje |
|---|---|
| `agent_run` · `agent_policy` | ponaglacz · strażnik świeżości · rozjemca · dyspozytor wyjątków · uzupełniacz · audytor cenników — każdy z bramką akceptacji i mierzalnym wynikiem |

**Repozytoria:** `temporalio/temporal` · `pydantic/pydantic-ai` · `crewAIInc/crewAI`

## M-61 · Dane rynkowe
**Spec:** `market.md` ← Aneks 2

| Obiekty | Funkcje kluczowe |
|---|---|
| `market_indicator` (+`is_redistributable`) · `market_observation` · `market_event` (warstwa 1/2/3) · `lane_risk_score` · `rate_forecast` · `forecast_evaluation` | **warstwa 1 deterministyczna: GRI, PSS, blank sailings, BAF ze wzoru, ETS** · warstwa 2 z backtestingiem przeciw random walk · warstwa 3 nigdy nie generuje liczby · alert ekspozycji |

**Repozytoria:** `Nixtla/statsforecast` · `unit8co/darts` · `facebook/prophet` · `Nixtla/neuralforecast` · `mlflow/mlflow` · `trafilatura`

## M-62 · Graf wiedzy o sieci
**Spec:** `ai.md` ← Aneks 4 §2.6

| Funkcje |
|---|
| który agent mocny na której relacji · który armator rolluje · wzorce zatorów · dziury w sieci |

**Repozytoria:** `microsoft/graphrag` · `pgvector/pgvector`

## M-63 · Symulacja portfela
**Spec:** `analytics.md` ← Aneks 4 §2.8

| Funkcje |
|---|
| „co jeśli stracę kontrakt z armatorem X" · „co jeśli paliwo +20%" · analiza scenariuszowa |

---

# DOMENA M — SPRZEDAŻ I KONTRAKTY

## M-64 · Przetargi
**Spec:** `tender.md` ← Aneks 5 §1

| Obiekty | Funkcje kluczowe |
|---|---|
| `tender` · `tender_lane` · `tender_bid_line` · `tender_outcome` | budowa oferty z żywej bazy stawek · kalendarz terminów · analiza wrażliwości · ryzyko zobowiązania 12-miesięcznego · historia przetargowa |

## M-65 · Kontrakty
**Spec:** `contracts.md` ← Aneks 5 §2–3

| Obiekty | Funkcje kluczowe |
|---|---|
| `contract` · `contract_adjustment` · `allocation` | **kontrakty indeksowane** (WCI/SCFI z korytarzem) · przeliczanie automatyczne · MQC z alertem niewykorzystania · podpowiadanie armatora z wolną alokacją |

## M-66 · Portal klienta
**Spec:** `portal.md`

| Funkcje |
|---|
| **osobna aplikacja SSR** · status, dokumenty, faktury, zapytanie · publiczny link trackingowy · widget wyceny na stronie klienta |

## M-67 · Rozliczanie subskrypcji
**Spec:** `billing.md`

| Obiekty | Funkcje |
|---|---|
| `subscription` · `usage_metric` (M-01) | abonament + per użytkownik + limit cenników · **model prowizji od odzysku z M-41** |

**Repozytoria:** `getlago/lago` · `killbill/killbill` · `stripe/stripe-python`

---

# DOMENA N — PLATFORMA

## M-68 · Obserwowalność
| Repozytoria |
|---|
| `open-telemetry/opentelemetry-python` (fundament) · `getsentry/sentry` · `langfuse/langfuse` · `PostHog/posthog` · `SigNoz/signoz` · `grafana/grafana` · `louislam/uptime-kuma` |

## M-69 · Jakość i wydajność
| Repozytoria |
|---|
| `import-linter` · `schemathesis/schemathesis` · `testcontainers/testcontainers-python` · `HypothesisWorks/hypothesis` · `grafana/k6` · `benfred/py-spy` · `bloomberg/memray` · `ankane/pghero` · `great-expectations/great_expectations` · `pact-foundation/pact-python` |

## M-70 · Wdrożenie
| Repozytoria |
|---|
| `emmett-framework/granian` · `postgresml/pgcat` · `citusdata/citus` · `pgbackrest/pgbackrest` · `minio/minio` · `coollabsio/coolify` · `traefik/traefik` · `renovatebot/renovate` · `qodo-ai/pr-agent` · `ariga/atlas` |
---

# PLAN BUDOWY v2 — 96 PLASTRÓW

Każdy plaster: `ID · moduł · zależności · zakres · warunek ukończenia`.
Kopiujesz do `docs/state/CURRENT.md`, otwierasz nową rozmowę z Cursorem.

---

## FAZA 0 · PLATFORMA (tydz. 1–3)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 0.1 | M-70 | — | Szkielet, granian, Docker Compose, justfile, CI | `just check/test/arch` przechodzi |
| 0.2 | — | 0.1 | Kompilacja aneksów → `docs/spec/` (70 modułów) | żaden plik > 400 linii |
| 0.3 | M-01 | 0.2 | `organization`, `app_user`, `role`, RLS, kontekst tenanta | test izolacji przechodzi |
| 0.4 | M-01 | 0.3 | `audit_log` triggerem, `usage_metric` | audyt bez udziału kodu aplikacji |
| 0.5 | M-02 | 0.3 | `outbox`, `idempotency_key`, publikator | zdarzenie przeżywa restart procesu |
| 0.6 | M-68 | 0.1 | OpenTelemetry, Sentry, Langfuse, PostHog | ślad przechodzi przez cały request |
| 0.7 | M-69 | 0.1 | import-linter, hypothesis, testcontainers, k6, budżety | naruszenie warstw wywala CI |
| 0.8 | M-04 | 0.3 | OpenFGA, model uprawnień, dostawca tożsamości | „handlowiec widzi swoich" działa |
| 0.9 | M-03 | 0.3 | `numbering_scheme`, `document_template`, `custom_field` | numeracja transakcyjna bez dziur |

## FAZA 1 · DANE I KONTRAHENCI (tydz. 4–6)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 1.1 | M-05 | 0.9 | `port` z improved-un-locodes, `location`, `terminal` | „Gdingen"→PLGDY działa |
| 1.2 | M-05 | 1.1 | World Port Index, strefy pocztowe per organizacja | strefy taryfowe konfigurowalne |
| 1.3 | M-06 | 0.9 | `charge_code` 60 kodów, aliasy 4 języki, `incoterm` | mapowanie alias→kod pokrywa próbkę |
| 1.4 | M-07 | 0.9 | `fx_rate`, NBP D-1, typ Money, trzy kursy | testy property-based przechodzą |
| 1.5 | M-10 | 1.3 | `party`, kontakty, rachunki, domeny mailowe | dodanie po NIP w 5 s |
| 1.6 | M-10 | 1.5 | GUS/REGON, VIES, biała lista | dane uzupełniają się automatycznie |
| 1.7 | M-09 | 1.3 | `hs_code`, powiązanie z kontrolą eksportu | — |
| 1.8 | M-08 | 1.3 | `dg_substance` z załączników ADR, segregacja | walidacja UN/klasa/grupa działa |

## FAZA 2 · STAWKI I WYCENA (tydz. 7–14)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 2.1 | M-17 | 1.5 | `rate_sheet`, `rate_line`, niemutowalność, `validity_basis` | 200 realnych pozycji w bazie |
| 2.2 | M-17 | 2.1 | Przedziały wagowe i LDM, `origin_context` | drobnica drogowa się mieści |
| 2.3 | M-18 | 2.1 | `port_charge_rule`, 11 wymiarów, `is_applicable` | reguła zerowa dla CIC z Europy działa |
| 2.4 | M-21 | 2.3 | **Silnik w SQL**: indeks pokrywający, dobór na cut-off | p95 < 300 ms na 50k wierszy |
| 2.5 | M-21 | 2.4 | `quotation_gap`, wykrywanie luk i wygasania | brakująca dopłata sygnalizowana |
| 2.6 | M-22 | 2.4 | `markup_rule`, kaskada 7 poziomów, narzut vs marża | widać, która reguła zadziałała |
| 2.7 | M-22 | 2.6 | `buy_source: customer_contract`, tryby prezentacji | kontrakt klienta z zerowym narzutem |
| 2.8 | M-23 | 2.6 | Tryby walutowe, klauzula, spread jako przychód | oferta wielowalutowa w obu trybach |
| 2.9 | M-26 | 2.8 | Szablon typst, dwa układy, „dlaczego ta cena" | PDF w obu układach |
| 2.10 | M-32 | 2.9 | Wysyłka z firmowej skrzynki, Graph/Gmail, podpis | widać w „Wysłanych" użytkownika |
| 2.11 | M-27 | 2.5 | Mapa pokrycia, wycena wsadowa | białe plamy widoczne |

### 🎯 PUNKT KONTROLNY — nagraj demo, wyślij trzem spedytorom

## FAZA 3 · TRACKING (tydz. 15–18)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 3.1 | M-19 | 1.5 | Framework kanałów, `carrier_credential` szyfrowane | drugi armator = konfiguracja |
| 3.2 | M-19 | 3.1 | Hapag: API pokrycia → `carrier_service` | wiadomo, kto ma serwis |
| 3.3 | M-36 | 3.2 | DCSA T&T, `shipment_event`, normalizacja | kontenery widoczne bez portalu |
| 3.4 | M-37 | 3.3 | **Watchdog free time**, rollover, poślizg ETA | alert przed pierwszą dobą demurrage |
| 3.5 | M-34 | 3.4 | Novu, push z akceptacją jednym dotknięciem | powiadomienie na telefon działa |
| 3.6 | M-36 | 3.3 | Mapa, publiczny link dla klienta | — |

## FAZA 4 · EKSTRAKCJA (tydz. 19–26)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 4.1 | M-32 | 2.10 | EmailEngine, odczyt własnych wątków, folder | brak dostępu poza wątkami i folderem |
| 4.2 | M-20 | 4.1 | 30 cenników w label-studio, promptfoo, langfuse | masz liczbę skuteczności |
| 4.3 | M-20 | 4.2 | Docling/Marker, porównanie na własnych plikach | wybór parsera na podstawie wyniku |
| 4.4 | M-20 | 4.3 | Instructor, schemat, `source_ref`, `unparsed_regions` | nic bez pochodzenia nie wchodzi |
| 4.5 | M-20 | 4.4 | llm-guard, presidio, router modeli | prompt injection w Excelu blokowany |
| 4.6 | M-20 | 4.4 | Normalizacja: alias→fuzzy→embedding | mapowanie opłat mierzalne |
| 4.7 | M-20 | 4.6 | Walidacja w kodzie, kolizje, anomalie jednostek | stawka −40% wymaga potwierdzenia |
| 4.8 | M-20 | 4.7 | Kolejka review, diff, akceptacja | nic nie wchodzi bez człowieka |
| 4.9 | M-20 | 4.8 | `extraction_template`, fingerprint, parser deterministyczny | powtórka bez modelu |
| 4.10 | M-06 | 4.8 | Uczenie aliasów z korekt | system uczy się słownika agenta |
| 4.11 | M-11 | 4.1 | `contact_suggestion`, podpis, podobne domeny | alert przy `andes-cargo.com` |

## FAZA 5 · PĘTLA ZAPYTAŃ (tydz. 27–34)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 5.1 | M-28 | 4.1 | Filtr po domenach klientów, `inbound_message` | widoczna tylko poczta klientów |
| 5.2 | M-28 | 5.1 | Klasyfikator wieloklasowy, progi, skrzynka propozycji | fałszywe pozytywy < kilka % |
| 5.3 | M-29 | 5.2 | Wykrywanie akceptacji oferty | akceptacja w piątek nie ginie |
| 5.4 | M-28 | 5.2 | Parsowanie dat: zakres + precyzja, 9 form zapisu | „połowa września" → 10–20.09 |
| 5.5 | M-28 | 5.2 | Wiele relacji, załączniki, języki, duplikaty, leady | pięć relacji = jedno rfq |
| 5.6 | M-28 | 5.5 | Notatka głosowa, formularz szybki, wklejanie | handlowiec rejestruje z telefonu |
| 5.7 | M-12 | 1.5 | `network`, `network_member` per tenant, import | katalog w tenancie |
| 5.8 | M-12 | 5.7 | Deduplikacja między sieciami | jeden agent = jeden rekord |
| 5.9 | M-30 | 5.7 | **Temporal**: workflow zapytania, timery, sygnały | restart nie gubi zapytania |
| 5.10 | M-30 | 5.9 | Okno wyboru, ranking, personalizacja 4 warstwy | mail wygląda na pisany do agenta |
| 5.11 | M-30 | 5.10 | Wysyłka indywidualna, token per odbiorca, rozłożenie | odpowiedź z innego adresu trafia |
| 5.12 | M-30 | 5.11 | Kaskada 4 poziomów dopasowania, przypomnienia | 4 poziomy pokryte testami |
| 5.13 | M-31 | 5.12 | Porównanie, wykrywanie braków, zapis jako rate_line | brak D/O fee oznaczony |
| 5.14 | M-13 | 5.13 | `party_scorecard` | ranking oparty na historii |
| 5.15 | M-30 | 5.9 | Uprzedzanie wygasających stawek | zapytanie idzie przed zapytaniem klienta |

## FAZA 6 · ZLECENIA I PIENIĄDZE (tydz. 35–46)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 6.1 | M-35 | 2.9 | Konwersja oferta→zlecenie, zamrożenie kwot | kurs i kwoty niezmienne |
| 6.2 | M-35 | 6.1 | Maszyna stanów, kontenery, zadania, SOP | statusy wymuszone |
| 6.3 | M-38 | 6.2 | Dokumenty, walidacja krzyżowa, draft B/L | niezgodność wykryta przed wysłaniem |
| 6.4 | M-40 | 6.2 | `invoice`, `bill`, KSeF 2.0, wizualizacja PDF | faktura wychodzi do KSeF |
| 6.5 | M-41 | 6.4 | **`cost_variance`**, raport rozbieżności | miesięczny raport odzysku |
| 6.6 | M-18 | 6.5 | **Uczenie reguł opłat portowych z faktur** | baza rośnie bez pracy operatora |
| 6.7 | M-42 | 6.4 | MT940, dopasowanie płatności | wpłaty łączą się z fakturami |
| 6.8 | M-43 | 6.7 | `FINCOST`, DSO/DPO, symulacja terminu | marża po koszcie kapitału na ofercie |
| 6.9 | M-44 | 6.8 | `FXDIFF`, ekspozycja netto przy wycenie | ostrzeżenie o ryzyku kursowym |
| 6.10 | M-45 | 6.8 | Prognoza kasowa, ekspozycja portfela, kaucje | raport tygodniowy |
| 6.11 | M-46 | 6.5 | `cost_to_serve`, trójwymiarowa rentowność | ranking klientów po realnym wyniku |
| 6.12 | M-24 | 6.9 | Marża zagrożona, optymalna ważność | sugestia okresu ważności |
| 6.13 | M-25 | 6.1 | `quotation_outcome`, elastyczność cenowa | krzywa marża/wygrana |

## FAZA 7 · ZGODNOŚĆ I AUTOMATYZACJA (tydz. 47–56)

| ID | Moduł | Zależy | Zakres | Ukończone gdy |
|---|---|---|---|---|
| 7.1 | M-53 | 1.5 | Listy UE/ONZ/OFAC/OFSI, pobieranie, wersjonowanie | codzienna aktualizacja działa |
| 7.2 | M-53 | 7.1 | Screening: transliteracja, fuzzy, whitelist | fałszywe trafienia zarządzalne |
| 7.3 | M-53 | 7.2 | **Przeskanowanie wszystkich przy zmianie listy** | nowe trafienie generuje alert |
| 7.4 | M-53 | 7.2 | Screening statków po IMO przed bookingiem | statek sprawdzany |
| 7.5 | M-54 | 6.7 | Zmiana rachunku z potwierdzeniem, podobne domeny | przelew na nowy rachunek blokowany |
| 7.6 | M-56 | 0.4 | Rejestr czynności, retencja, eksport tenanta | eksport na żądanie działa |
| 7.7 | M-19 | 3.2 | Hapag Quick Quotes + Spot | live spot obok cennika |
| 7.8 | M-19 | 7.7 | Maersk Offers, wymogi UI armatora | oferta zgodna z wytycznymi |
| 7.9 | M-19 | 7.8 | CMA CGM, uzupełnianie opłat lokalnych z bazy | niepełna oferta oznaczona |
| 7.10 | M-21 | 7.7 | SSE, strumieniowanie wyników, degradacja | wyniki spływają przyrostowo |
| 7.11 | M-19 | 7.7 | Kanał mailowy dla armatorów bez API | zasięg nieograniczony |
| 7.12 | M-03 | 7.10 | `quote_automation_policy`, tryby manual/assisted/auto | wybór per klient i relacja |
| 7.13 | M-34 | 7.12 | Push z akceptacją, `auto_quote_policy` z bezpiecznikami | oferta o 22:16 |

## FAZA 8 · GAŁĘZIE I ROZSZERZENIA (tydz. 57–72)

| ID | Moduł | Zakres |
|---|---|---|
| 8.1 | M-48 | `tour`, `tour_assignment`, alokacja shared/capacity |
| 8.2 | M-48 | Tryb marginal, koszt krańcowy doładunku, puste powroty |
| 8.3 | M-48 | Alokacja → `shipment_charge`, pętla zwrotna do marż |
| 8.4 | M-48 | or-tools, 3D bin packing, PyVRP |
| 8.5 | M-51 | `lcl_rate`, W/M, minimum, cut-off CFS |
| 8.6 | M-51 | Próg opłacalności LCL vs FCL |
| 8.7 | M-51 | Konsolidatorzy jako kanał |
| 8.8 | M-49 | `rail_operator`, `rail_service`, kanał mailowy |
| 8.9 | M-52 | `emission_factor`, GLEC/ISO 14083 |
| 8.10 | M-49 | Porównanie droga/kolej z emisją |
| 8.11 | M-50 | Kolej z Chin, korytarze, `route_sanctions_check` |
| 8.12 | M-39 | IFTMIN, IFTSTA, AS2 |
| 8.13 | M-55 | Reklamacje z terminami zawitymi |
| 8.14 | M-16 | `customer_sop` generujące zadania |

## FAZA 9 · WARSTWA AI I SPRZEDAŻ (tydz. 73+)

| ID | Moduł | Zakres |
|---|---|---|
| 9.1 | M-57 | Serwer MCP, narzędzia odczytowe i zapisowe z bramką |
| 9.2 | M-59 | WrenAI + Cube + sqlglot, replika do odczytu |
| 9.3 | M-58 | CopilotKit w interfejsie |
| 9.4 | M-60 | Cyfrowi współpracownicy — sześciu agentów z bramkami |
| 9.5 | M-14 | Wywiadownie, KRS, RDF, KRZ, MSiG |
| 9.6 | M-15 | Wirtualny CFO: scoring, limit, termin, notatka |
| 9.7 | M-61 | Dane rynkowe warstwa 1: GRI, PSS, blank sailings, BAF, ETS |
| 9.8 | M-61 | Warstwa 2 z backtestingiem, warstwa 3 kontekstowa |
| 9.9 | M-64 | Przetargi: `tender`, analiza wrażliwości, historia |
| 9.10 | M-65 | Kontrakty indeksowane, MQC, alokacja |
| 9.11 | M-66 | Portal klienta jako osobna aplikacja SSR |
| 9.12 | M-33 | Dodatek do Outlooka |
| 9.13 | M-62 | Graf wiedzy o sieci |
| 9.14 | M-63 | Symulacja portfela |
| 9.15 | M-67 | Rozliczanie subskrypcji, model prowizji od odzysku |
| 9.16 | M-47 | Integracja księgowa |

---

## STATYSTYKA

| | Liczba |
|---|---|
| Moduły | 70 |
| Obiekty danych | ~130 |
| Plastry | 96 |
| Repozytoria przypisane | ~180 z katalogu 407 |
| Fazy | 10 |

**Fazy 0–3 (18 tygodni) dają produkt sprzedawalny.** Reszta to rozbudowa,
której kolejność powinni wskazać klienci — plan 8 i 9 traktuj jako zbiór
gotowych do podjęcia, nie jako sekwencję do przerobienia w całości.
