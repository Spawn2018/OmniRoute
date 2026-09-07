# Katalog pól — wizja operatora 2026-09-07

**Status:** szkic wejściowy do `/plan-modul`. Zero kodu produktu. Finalne nazwy kolumn i cięcie do jednego plastra ustala Plan modułu.  
**Fale** = [PLAN-REALIZACJA.md](../PLAN-REALIZACJA.md) § Kolejka (pin 2026-09-08). Kopia robocza: [kolejka-propozycja.md](kolejka-propozycja.md).  
**Sprawdzenie kolumn:** model BC + najnowsza migracja tej tabeli. Brak zgadywania.  
**Nie jest:** plaster ani `/noc`.

## Legenda

| Kolumna | Znaczenie |
|---|---|
| Pole | nazwa EN z GLOSSARY, albo propozycja EN (domena) |
| Typ | jak w repo: `Numeric` nie float; kwota = para amount+currency; współrzędne jak `location.lat`/`lng` |
| Obowiązkowe | na wierszu domenowym po zapisie (nie na szkicu HITL) |
| Źródło | API zewnętrzne / HITL / operator / SQL (wyliczenie, nie model) |
| Fala | ID z kolejki-propozycji |
| Już w kodzie? | `ISTNIEJE` + dokładna kolumna/ścieżka **albo** `NIE` |

**HC na każdym nowym obiekcie (nie powtarzane w każdym wierszu):** `organization_id` UUID NOT NULL + RLS FORCE + test izolacji; `id` UUID PK; `source_ref` text NOT NULL tam, gdzie rekord wchodzi z zewnątrz albo od operatora; `created_at` / `updated_at` / `created_by` jak `TimestampMixin` (ISTNIEJE wzorzec w `backend/app/models/base.py`). Sekrety: ciphertext kluczem tenanta, **nie** `organization_setting` (allowlista odrzuca `api_key` / `secret` / `password` / `token`).

**Nie dublować:** `tracking_event` ≠ `position_event`. `party_scorecard` ≠ snapshot Trans.eu. `shipment_document` ≠ `party_document` ≠ `document_template`. `quotation_print_template` (M-03, token `plain`/`letter`) ≠ silnik `document_template` (D9). `entity_event` (B0, szyna append-only) może kiedyś połknąć część zdarzeń — Plan tnie; tu zostają nazwane obiekty z rozmowy.

---

## 1. Tenancy / RLS / ustawienia

### 1.1 Wzorzec (już w kodzie)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `organization_id` | UUID FK → `organization` | tenant; RLS | tak | sesja | fundament | ISTNIEJE na każdej tabeli biznesowej |
| `organization.slug` | text | slug tenanta | tak | operator | fundament | ISTNIEJE `organization.slug` |
| `app_user.id` | UUID | użytkownik w tenancie | tak | operator | fundament | ISTNIEJE `app_user.id` |

### 1.2 `organization_setting` (M-03) — klucze, nie nowe kolumny

Tabela ISTNIEJE: `setting_key` VARCHAR(64), `setting_value` VARCHAR(64). Nowe potrzeby = **nowy klucz w allowliście**, o ile wartość mieści się w 64 znakach. Zestaw dokumentów blokujących = osobna tabela (1.3), nie JSON w `setting_value`.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `default_currency` | CHAR(3) jako wartość | domyślna waluta tenanta | tak gdy klucz istnieje | operator | M-03 | ISTNIEJE klucz `default_currency` |
| `quotation_number_prefix` | text ≤16 | prefiks numeru oferty | nie | operator | M-26 | ISTNIEJE klucz `quotation_number_prefix` |
| `quotation_print_template` | enum `plain`/`letter` | szablon druku oferty (token) | nie | operator | M-26 | ISTNIEJE klucz `quotation_print_template` |
| `telematics_grace_days` | int jako tekst, default `3` | **dni robocze** bez trip na `external_api` (nie kalendarzowe; nie dotyczy `omni_telematic`) | tak gdy telematyka włączona | operator | V5 | NIE |
| `hitl_confidence_green` | Numeric 0–1, default `0.85` | próg zielony zbiorczego accept | tak | operator | X9 | NIE |
| `hitl_confidence_amber` | Numeric 0–1, default `0.70` | poniżej: bez accept zbiorczego | tak | operator | X9 | NIE |
| `invoice_match_suggest_min` | Numeric 0–1 | próg „1-klik accept” (jedna kandydatura) | tak | operator | F10 | NIE |
| `invoice_match_rank_max` | int, default `8` | max pozycji rankingu HITL | tak | operator | F10 | NIE |
| `trans_risk_block_threshold` | text token | próg blokady po TransRisk (dane, nie twardy kod) | nie | operator | C9 | NIE |
| `ocean_inquiry_default_n` | int jako tekst, default `3` | ile agentów zaznaczonych na starcie (max 8) | tak gdy Fala O | operator | O4 | NIE |
| `ocean_inquiry_rank_max` | int jako tekst, default `8` | sufit listy rankingu zapytań | tak gdy Fala O | operator | O4 | NIE |
| `ocean_scorecard_window_days` | int jako tekst, default `90` | okno SQL `party_lane_scorecard` | tak gdy Fala O | operator | O5 | NIE |

### 1.3 `relation_document_requirement` — NOWA tabela

Wymagany zestaw `party_document` per relacja (krajowa / międzynarodowa / odpad). Nie scoring osoby.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `relation_kind` | enum `domestic` / `international` / `waste` | rodzaj relacji, dla której brama 409 | tak | operator | C8 | NIE |
| `document_kind` | enum jak `party_document.document_kind` | który dokument jest wymagany | tak | operator | C8 | NIE |
| `blocks_create` | bool | brak/unpaid/po terminie → 409 na `POST shipment` i przypisaniu podwykonawcy | tak | operator | C8 | NIE |
| `source_ref` | text | pochodzenie reguły | tak | operator | C8 | NIE |

---

## 2. Shipment / trip / płyta / stop

`trip` i `resource` są w kartach Fali T; okno obserwacji GPS (§13g) **wisi na trip + płycie**, nie na flotie 24/7. `stop` jest potrzebny, bo warunek stopu polla to `last_stop.completed`.

### 2.1 `shipment` — rozszerzenie (tabela ISTNIEJE, migracja `049` + model)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `id` | UUID | zlecenie | tak | system | M-35 | ISTNIEJE `shipment.id` |
| `quotation_id` | UUID FK | wycena źródłowa | tak | system | M-35 | ISTNIEJE `shipment.quotation_id` |
| `party_id` | UUID FK | kontrahent zlecenia | tak | operator | M-35 | ISTNIEJE `shipment.party_id` |
| `source_ref` | text | pochodzenie wiersza | tak | operator/system | M-35 | ISTNIEJE `shipment.source_ref` |
| `status` | text, dziś tylko `draft` | status zlecenia | tak | operator | M-35 | ISTNIEJE `shipment.status` |
| `shipment_ref` | text, unikat per tenant | twardy numer na wydruku, QR, mailu, FV podwykonawcy | tak | system (szablon M-03) | F10 + D9 | NIE |
| `is_waste` | bool | ładunek odpadu (nakłada się z SENT) | tak | operator / HITL | C6 | NIE |

### 2.2 `resource` — NOWA tabela (płyta / kierowca / naczepa)

Jedna tabela z `kind` (wzorzec Qargo z kart T2). Toll (§13h) czyta klasę pojazdu stąd.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `kind` | enum `vehicle` / `driver` / `trailer` | rodzaj zasobu | tak | operator | T2 | NIE |
| `name` | text | nazwa wyświetlana | tak | operator | T2 | NIE |
| `registration_no` | text | płyta rejestracyjna (klucz mapowania adaptera GPS) | tak gdy `kind=vehicle` | operator / API płyty | T2 + V5 | NIE |
| `inventory_no` | text | nr inwentarzowy | nie | operator | T2 | NIE |
| `gvm_kg` | Numeric ≥ 0 | DMC — wejście myta | nie | operator | V2b | NIE |
| `axle_count` | int ≥ 0 | liczba osi — myto | nie | operator | V2b | NIE |
| `euro_emission_class` | text | klasa Euro | nie | operator | V2b | NIE |
| `co2_class` | text | klasa CO₂ taryfy 2022/62/WE | nie | operator | V2b | NIE |
| `source_ref` | text | pochodzenie | tak | operator | T2 | NIE |

### 2.3 `trip` — NOWA tabela

Jednostka wykonawcza; start/stop okna GPS.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `trip_no` | text | numer tripa z szablonu M-03 | tak | system | T2 | NIE |
| `status` | enum `draft` / `planned` / `in_transit` / `completed` / `cancelled` | status wykonania | tak | operator | T2 | NIE |
| `vehicle_resource_id` | UUID FK → `resource` | przypisana płyta; `assigned` startuje poll | nie | operator | T2 + V5 | NIE |
| `trailer_resource_id` | UUID FK → `resource` | naczepa | nie | operator | T2 | NIE |
| `driver_resource_id` | UUID FK → `resource` | kierowca I | nie | operator | T2 | NIE |
| `subcontractor_party_id` | UUID FK → `party` | podwykonawca (brama C8 przy przypisaniu) | nie | operator | T2 + C8 | NIE |
| `assigned_at` | timestamptz | moment przypisania pojazdu = start obserwacji | nie | system | V5 | NIE |
| `observation_started_at` | timestamptz | faktyczny start poll/subscribe | nie | system/API | V5 | NIE |
| `last_stop_completed_at` | timestamptz | ostatni stop `completed` — początek grace | nie | system | V5 | NIE |
| `observation_ends_at` | timestamptz | `last_stop_completed_at` + grace; po tym live gaśnie | nie | SQL | V5 | NIE |
| `route_geometry` | text/bytea (WKT/WKB, nie float-JSON) | geometria trasy do pogody i myta | nie | API routingu / operator | V2 + V2b | NIE |
| `source_ref` | text | pochodzenie | tak | operator | T2 | NIE |

### 2.4 `stop` — NOWA tabela (minimum pod okno GPS)

Pełna karta T1 zostaje w `karty-pol-fala-t.md`. Tu tylko pola, bez których §13g nie działa.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `shipment_id` | UUID FK → `shipment` | zlecenie punktu | tak | operator | T1 | NIE |
| `trip_id` | UUID FK → `trip` | trip spinający stopy | nie | operator | T1 + T2 | NIE |
| `sequence_no` | int ≥ 0 | kolejność; max completed = last_stop | tak | operator | T1 | NIE |
| `location_id` | UUID FK → `location` | miejsce ze słownika (nie luźny adres) | tak | operator / resolve M-05 | T1 | NIE |
| `kind` | enum m.in. `loading` / `unloading` / `customs` / `ferry` / `terminal` / `depot` / `other` | typ punktu | tak | operator | T1 | NIE |
| `status` | enum `pending` / `at_stop` / `completed` / `failed` | status; `completed` zamyka okno po grace | tak | operator / API / apka | T1 + V5 | NIE |
| `completed_at` | timestamptz | kiedy stop ukończony | nie | operator / API | V5 | NIE |
| `source_ref` | text | pochodzenie | tak | operator/API | T1 | NIE |

`location.lat` / `location.lng` — ISTNIEJE `Numeric(8,6)` / `Numeric(9,6)` na `location` (model geography). Pogoda i GPS **nie** nadpisują tych kolumn floatem.

### 2.5 `shipment_leg` — bez nowych kolumn w tej wizji

ISTNIEJE: `leg_kind` (`road`/`rail`/`china_rail`/`ocean_lcl`), `origin_location_id`, `destination_location_id`, `source_ref`. Trip nie zastępuje nogi; Plan T2 rozdziela.

---

## 3. Telematyka

`tracking_event` (M-36) zostaje śladem operacyjnym `departed`/`arrived`/`noted` na `shipment` — **nie** pozycją GPS.

### 3.1 `tracking_event` — istnieje, nie rozszerzać o GPS

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `event_kind` | enum `departed`/`arrived`/`noted` | rodzaj zdarzenia operacyjnego | tak | operator | M-36 | ISTNIEJE `tracking_event.event_kind` |
| `occurred_at` | timestamptz | kiedy | tak | operator | M-36 | ISTNIEJE `tracking_event.occurred_at` |
| `shipment_id` | UUID FK | zlecenie | tak | operator | M-36 | ISTNIEJE `tracking_event.shipment_id` |
| `source_ref` | text | pochodzenie | tak | operator | M-36 | ISTNIEJE `tracking_event.source_ref` |

### 3.2 `position_event` — NOWA tabela (kontrakt PositionEvent)

Normalizacja ze wszystkich adapterów. Współrzędne `Numeric` jak `location`. Historia z okresu zlecenia zostaje; live gaśnie z oknem trip.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `trip_id` | UUID FK → `trip` | trip w oknie obserwacji | tak | system | V5 | NIE |
| `resource_id` | UUID FK → `resource` | płyta, której dotyczy punkt | tak | adapter | V5 | NIE |
| `recorded_at` | timestamptz | czas pomiaru u źródła | tak | API | V5 | NIE |
| `lat` | Numeric(8,6) | szerokość | tak | API | V5 | NIE |
| `lng` | Numeric(9,6) | długość | tak | API | V5 | NIE |
| `heading_deg` | Numeric | kurs | nie | API | V5 / 13j UTM | NIE |
| `speed_kmh` | Numeric ≥ 0 | prędkość | nie | API | V5 | NIE |
| `altitude_m` | Numeric | wysokość (osobno od pogody) | nie | API | V5 / 13j | NIE |
| `fuel_l` | Numeric ≥ 0 | paliwo — flaga anomalii to recenzja, nie wyrok | nie | API | V5 / 13j | NIE |
| `cargo_temp_c` | Numeric | temperatura ładunku | nie | API | V5 / 13j | NIE |
| `dtc_code` | text | kod diagnostyczny CAN | nie | API | 13j UTM | NIE |
| `provider_code` | text token | gbox / ikol / flotis / wialon / trans_eu / timocom / transporeon / driver_app / sms / aggregator | tak | adapter | V5 | NIE |
| `adapter_level` | enum `L0` / `L1a` / `L1b` / `L1c` / `exchange` | warstwa źródła | tak | system | V5 | NIE |
| `provider_eta_at` | timestamptz | ETA **podana przez API** (nie liczona u nas) | nie | API | V5b | NIE |
| `source_ref` | text | które API, które żądanie, idempotencja | tak | adapter | V5 | NIE |

### 3.3 `telematics_connector` — NOWA tabela (adapter + sekrety)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `provider_code` | text | dostawca / aggregator | tak | operator | V5 | NIE |
| `protocol` | text | REST/SOAP/SDK — dane, nie enum w kodzie na zawsze | tak | operator | V5 | NIE |
| `credential_ciphertext` | bytea | poświadczenia BYO, klucz tenanta | tak gdy BYO | operator | V5 | NIE |
| `external_account_ref` | text | identyfikator konta u dostawcy (nie hasło) | nie | operator | V5 | NIE |
| `is_aggregator` | bool | Linkway / DRIP vs native | tak | operator | V5 | NIE |
| `is_enabled` | bool | czy poll wolno odpalić | tak | operator | V5 | NIE |
| `source_ref` | text | pochodzenie konfiguracji | tak | operator | V5 | NIE |

P0 native (dokumentacja publiczna): GBOX, IKOL, Flotis, Wialon. Reszta = aggregator albo umowa.

### 3.4 `resource_telematics_link` — NOWA tabela (płyta → konto GPS)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `resource_id` | UUID FK | pojazd | tak | operator / API | V5 | NIE |
| `connector_id` | UUID FK | które konto adaptera | tak | operator | V5 | NIE |
| `external_asset_id` | text | ID pojazdu u dostawcy | tak | API / operator | V5 | NIE |
| `observation_kind` | enum `omni_telematic` / `external_api` | pakiet Omni + umowa vs BYO GPS | tak | operator | V5 | NIE |
| `observation_status` | enum `idle` / `active` / `grace` / `stopped` | external: grace = 3 dni robocze; omni_telematic = active floty | tak | system | V5 | NIE |
| `current_trip_id` | UUID FK | trip w aktywnym oknie (external) | nie | system | V5 | NIE |
| `source_ref` | text | pochodzenie wiązania | tak | operator/API | V5 | NIE |

### 3.5 `exchange_message` — NOWA tabela (giełda, tylko gdy tenant jest stroną)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `exchange_code` | text | trans_eu / timocom / … | tak | API / eksport | V5b | NIE |
| `external_id` | text | id wiadomości u giełdy; idempotencja | tak | API | V5b | NIE |
| `party_id` | UUID FK | druga strona | nie | resolve | V5b | NIE |
| `carrier_inquiry_id` | UUID FK | ślad kupna M-30 | nie | operator | V5b | NIE |
| `direction` | enum `in` / `out` | kierunek | tak | API | V5b | NIE |
| `occurred_at` | timestamptz | czas | tak | API | V5b | NIE |
| `source_ref` | text | oficjalne API/eksport; zakaz scrapingu | tak | API | V5b | NIE |

Treść → `extraction_draft` HITL → `rate_line`. Nie skrapować czatu.

### 3.6 `carrier_inquiry` — rozszerzenie (tabela ISTNIEJE, migracja `043`)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `network_member_id` | UUID FK | agent w sieci | tak | operator | M-30 | ISTNIEJE `carrier_inquiry.network_member_id` |
| `status` | text, dziś `draft` | status śladu | tak | operator | M-30 | ISTNIEJE `carrier_inquiry.status` |
| `source_ref` | text | pochodzenie | tak | operator | M-30 | ISTNIEJE `carrier_inquiry.source_ref` |
| `quoted_amount` | Numeric(14,4) | cena z **naszego** maila/czatu/API (nie cudzy podsłuch) | nie | operator / HITL | V5b / O3 | NIE |
| `quoted_currency` | CHAR(3) | waluta cytowanej ceny; para z amount | tak gdy amount | operator / HITL | V5b / O3 | NIE |
| `origin_port_id` | UUID FK → `port` | POL zapytania | tak od O3 | operator | O3 | NIE |
| `destination_port_id` | UUID FK → `port` | POD zapytania | tak od O3 | operator | O3 | NIE |
| `quoted_transit_days` | int ≥ 1 nullable | TT z odpowiedzi | nie | HITL / operator | O3 | NIE |
| `sent_at` / `answered_at` | timestamptz nullable | pomiar odpowiedzi | nie | system | O3 | NIE |

### 3.7 `entity_event` — NOWA tabela (szyna B0 / historia w oknie trip)

Append-only. Plan V5 decyduje, czy `position_event` jest kindiem tutaj, czy osobną tabelą. W katalogu: osobny obiekt + ta szyna na metryki jobu spedytora i pogodę jako czynnik (nie liczba z LLM).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `subject_kind` | text | `trip` / `quotation` / `carrier_inquiry` / … | tak | system | B0 | NIE |
| `subject_id` | UUID | obiekt | tak | system | B0 | NIE |
| `event_kind` | text | np. `weather_factor`, `first_reply`, `offer_view` | tak | system/API | B0 + V5 | NIE |
| `occurred_at` | timestamptz | kiedy | tak | system | B0 | NIE |
| `source_ref` | text | pochodzenie | tak | system | B0 | NIE |

### 3.8 `weather_observation` — NOWA tabela (Open-Meteo wzdłuż geometrii)

Nie jeden punkt „kraj załadunku”. Nie wejście do marży. LLM nie liczy ETA z tych pól.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `trip_id` | UUID FK | trip, wzdłuż którego próbkowano | tak | system | V2 | NIE |
| `sequence_no` | int | kolejność punktu na geometrii | tak | system | V2 | NIE |
| `lat` | Numeric(8,6) | punkt próbki | tak | system | V2 | NIE |
| `lng` | Numeric(9,6) | punkt próbki | tak | system | V2 | NIE |
| `sampled_at` | timestamptz | czas prognozy/obserwacji | tak | API | V2 | NIE |
| `weather_code` | int/text | kod WMO / źródła | tak | API | V2 | NIE |
| `temperature_c` | Numeric | temperatura | nie | API | V2 | NIE |
| `wind_speed_ms` | Numeric ≥ 0 | wiatr | nie | API | V2 | NIE |
| `precipitation_mm` | Numeric ≥ 0 | opad | nie | API | V2 | NIE |
| `provider_code` | text | `open_meteo` / `imgw` / `dwd` / `meteo_france` | tak | adapter | V2 | NIE |
| `source_ref` | text | które API, która siatka, idempotencja | tak | API | V2 | NIE |

---

## 4. Compliance (dokumenty, SENT-EU, myto, Trans.eu)

### 4.1 `party_document` — NOWA tabela

Niemutowalna historia: odblokowanie = **nowy** wiersz. Stary zostaje.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `party_id` | UUID FK → `party` | czyj dokument | tak | operator | C8 | NIE |
| `document_kind` | enum `ocp` / `ocs` / `comm_insurance` / `community_licence` / `cemt` / `bdo_number` / `waste_permit` / `other` | rodzaj (inne = dane, nie twardy kod) | tak | operator / HITL / API Trans.eu | C8 | NIE |
| `document_no` | text | numer polisy / licencji / BDO | nie | operator / HITL | C8 + C6 | NIE |
| `valid_from` | date | początek ważności | tak | operator / HITL | C8 | NIE |
| `valid_to` | date | koniec; `<` data załadunku → 409 | tak | operator / HITL / `documents.expire_date` | C8 | NIE |
| `premium_status` | enum `paid` / `unpaid` / `unknown` | składka; `unpaid` → 409 | tak | operator / HITL | C8 | NIE |
| `source_ref` | text | upload / extract / Trans.eu | tak | HITL / API / operator | C8 | NIE |

`party` ISTNIEJE (`legal_name`, `tax_id`, `roles`, `source_ref`, …). Nie dopisywać scoringu na `party`.

### 4.2 `party_exchange_snapshot` — NOWA tabela

Nie mylić z `party_scorecard` (ISTNIEJE: `response_rate`, `median_response_hours`, `price_position`, `quote_invoice_match_rate`, `rollover_count`).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `party_id` | UUID FK | kontrahent | tak | system | C9 | NIE |
| `overall_rating` | Numeric 0–5 | ocena Partners API Trans.eu | nie | API | C9 | NIE |
| `trans_risk` | text | SUPER…POOR | nie | API | C9 | NIE |
| `payments_status` | text | status płatności z API | nie | API | C9 | NIE |
| `satisfaction_json` | JSONB | communication, documents_delivery, … | nie | API | C9 | NIE |
| `fetched_at` | timestamptz | kiedy pobrano snapshot | tak | system | C9 | NIE |
| `source_ref` | text | endpoint + czas; zakaz scrapingu opinii | tak | API | C9 | NIE |

Komentarze słowne: tylko po oficjalnym API/eksporcie albo wklejenie HITL — osobne pole `comment_text` **nie** wchodzi, dopóki TO_VERIFY endpointu.

### 4.3 `monitoring_scheme` — NOWA tabela (katalog SENT-EU)

Kopia per tenant. Brak klona w kraju ≠ wymyślony wiersz.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `country_code` | CHAR(2) | ISO kraju (albo `EU` dla EMCS/NCTS/DIWASS/eFTI) | tak | operator / seed | C7 | NIE |
| `scheme_code` | text snake | `sent`, `sent_geo`, `ekaer`, `bireg`, `ro_e_transport`, `emcs`, `ncts`, `e_tir`, `diwass`, `efti`, `trackdechets`, `rentri`, `silicie`, `atlas`, `bdo_kpo` | tak | seed po źródle prawnym | C7 | NIE |
| `authority_name` | text | urząd (PUESC, …) | tak | seed | C7 | NIE |
| `has_geo` | bool | czy wymaga GPS na czas zgłoszenia | tak | seed | C7 | NIE |
| `api_kind` | text | `official` / `checklist_only` / `unset` | tak | seed | C7 | NIE |
| `is_legally_confirmed` | bool | fałsz = nie adapter | tak | seed | C7 | NIE |
| `source_ref` | text | akt / URL dokumentacji | tak | seed | C7 | NIE |

### 4.4 `shipment_monitoring_filing` — NOWA tabela

Numery i statusy zgłoszenia na zleceniu (Omni nie zastępuje BDO/SENT).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `shipment_id` | UUID FK | zlecenie | tak | operator | C1 + C6 + C7 | NIE |
| `monitoring_scheme_id` | UUID FK | który system | tak | operator | C7 | NIE |
| `filing_ref` | text | numer SENT / KPO / UIT / ARC | nie | API / HITL / operator | C1 + C6 | NIE |
| `status` | text | status urzędowy (dane) | tak | API / operator | C1 | NIE |
| `geo_required` | bool | kopia z scheme w chwili zgłoszenia | tak | system | C1 | NIE |
| `valid_from` | timestamptz | okno zgłoszenia | nie | API | C1 | NIE |
| `valid_to` | timestamptz | koniec obowiązku GEO | nie | API | C1 | NIE |
| `source_ref` | text | HITL przed zapisem z extractu | tak | HITL / API | C1 + C6 | NIE |

### 4.5 Myto — `charge` + katalog `charge_code` (nie druga marża)

`charge` ISTNIEJE (`009`): `charge_code`, `buy_amount`, `buy_currency`, `sell_amount`, `sell_currency`, `rate_line_id`. **Brak `source_ref` na `charge`.** Winieta ≠ km = dwa kody w katalogu M-06, nie dwa magazyny marży.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `charge_code` | text | token katalogu (osobno winieta vs km) | tak | operator / SQL | M-06 + V2b | ISTNIEJE `charge.charge_code` |
| `buy_amount` | Numeric(14,4) | kupno | tak | operator / SQL z taryfy | M-08 | ISTNIEJE `charge.buy_amount` |
| `buy_currency` | CHAR(3) | waluta kupna | tak | operator | M-08 | ISTNIEJE `charge.buy_currency` |
| `sell_amount` | Numeric(14,4) | sprzedaż | tak | operator | M-08 | ISTNIEJE `charge.sell_amount` |
| `sell_currency` | CHAR(3) | = buy_currency | tak | operator | M-08 | ISTNIEJE `charge.sell_currency` |
| `rate_line_id` | UUID FK nullable | źródło stawki | nie | system | M-08 | ISTNIEJE `charge.rate_line_id` |
| `source_ref` | text | które API myta, która taryfa, która data | tak | API / operator | V2b | NIE (luka vs HC-05 analog + §13h) |

Brak taryfy = warning, nie zmyślona kwota. LLM/JS nie liczą.

`rate_line.source_ref` — ISTNIEJE. Ekstrakcja stawki z `exchange_message` kończy się tu po HITL.

---

## 5. Maps

### 5.1 `map_basemap` — NOWA tabela (katalog podkładów jako dane)

Nie sztywny enum w kodzie. Zakaz `tile.openstreetmap.org` jako CDN: `is_blocked=true` na tym URL.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `basemap_code` | text | openfreemap / opentopomap / cyclosm / hot / carto_positron / gugik_ortho / esri_imagery / mapbox / … | tak | seed | X8 | NIE |
| `kind` | enum `free` / `paid_byo` / `self_host` | darmowy / klucz admina / PMTiles | tak | seed | X8 | NIE |
| `tile_url_template` | text | szablon kafelka / style JSON | tak | seed | X8 | NIE |
| `attribution` | text | obowiązkowa atrybucja na dole mapy | tak | seed | X8 | NIE |
| `requires_key` | bool | czy admin musi wkleić sekret | tak | seed | X8 | NIE |
| `is_blocked` | bool | np. osm.org tiles | tak | seed | X8 | NIE |
| `source_ref` | text | polityka licencji | tak | seed | X8 | NIE |

### 5.2 `user_map_prefs` — NOWA tabela

Bez kluczy API. `table_view` (ISTNIEJE) zostaje na siatki, nie na mapę.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `user_id` | UUID FK → `app_user` | czyje preferencje | tak | sesja | X8 | NIE |
| `last_basemap_code` | text | ostatnio wybrany podkład | nie | użytkownik | X8 | NIE |
| `enabled_basemap_codes` | text[] / JSONB | które darmowe włączone | tak | użytkownik | X8 | NIE |
| `overlay_opacity` | Numeric 0–1 | przezroczystość nakładek | tak | użytkownik | X8 | NIE |
| `overlay_traffic` | bool | nakładka ruchu | tak | użytkownik | X8 | NIE |
| `overlay_lez` | bool | LEZ / restrykcje | tak | użytkownik | X8 | NIE |
| `overlay_rail` | bool | OpenRailwayMap | tak | użytkownik | X8 | NIE |

### 5.3 `tenant_map_provider` — NOWA tabela (płatne BYO)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `basemap_code` | text FK logiczny do katalogu | Mapbox, HERE, PTV, … | tak | admin | X8 | NIE |
| `style_ref` | text | który styl u dostawcy | nie | admin | X8 | NIE |
| `credential_ciphertext` | bytea | klucz; nigdy w logach | tak | admin | X8 | NIE |
| `domain_restriction` | text | domena z panelu dostawcy | nie | admin | X8 | NIE |
| `is_enabled` | bool | czy zespół widzi podkład | tak | admin | X8 | NIE |
| `source_ref` | text | kto zapisał | tak | admin | X8 | NIE |

---

## 6. ERP

Omni wystawia FV (KSeF = Omni). ERP księguje. Adapter nie liczy VAT/marży. `ksef_issuer` = stała `omni` — **nie kolumna** (decyzja 2026-09-07). `bookkeeping` ISTNIEJE jako para `charge_id` + `sales_invoice_id` (nie FZ).

### 6.1 `erp_connector` — NOWA tabela

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `system_code` | text | `comarch_optima` / `comarch_xl` / `symfonia` / `subiekt_nexo` / `subiekt_gt` / … | tak | admin | F9 | NIE |
| `protocol` | text | COM / CDN / REST / Sfera — dane | tak | admin | F9 | NIE |
| `base_url` | text | URL WebAPI / adres agenta | nie | admin | F9 | NIE |
| `requires_agent` | bool | outbound agent on-prem | tak | admin | F9 | NIE |
| `credential_ciphertext` | bytea | klucz aplikacji / operator Sfery | tak | admin | F9 | NIE |
| `is_enabled` | bool | sync włączony | tak | admin | F9 | NIE |
| `source_ref` | text | pochodzenie | tak | admin | F9 | NIE |

### 6.2 `erp_series_map` — NOWA tabela (HITL pierwszego mapowania)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `connector_id` | UUID FK | które FK | tak | admin | F9 | NIE |
| `omni_document_kind` | enum `sales_invoice` / `purchase_invoice` | FS vs FZ | tak | admin | F9 | NIE |
| `erp_series` | text | seria w Comarch/Symfonii/Subiekcie | tak | HITL księgowy | F9 | NIE |
| `gl_account` | text | konto dekretu | nie | HITL księgowy | F9 | NIE |
| `accepted_by` | UUID FK → `app_user` | kto zatwierdził mapowanie | tak | HITL | F9 | NIE |
| `source_ref` | text | pochodzenie | tak | HITL | F9 | NIE |

### 6.3 `erp_export` — NOWA tabela (status z ERP, bez nadpisu kwot)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `connector_id` | UUID FK | connector | tak | system | F9 | NIE |
| `document_kind` | enum `sales_invoice` / `purchase_invoice` | który strumień | tak | system | F9 | NIE |
| `document_id` | UUID | id dokumentu Omni | tak | system | F9 | NIE |
| `erp_journal_ref` | text | numer w dzienniku FK | nie | ERP → Omni | F9 | NIE |
| `payment_status` | text | status płatności z ERP | nie | ERP → Omni | F9 | NIE |
| `exported_at` | timestamptz | kiedy wysłano | nie | system | F9 | NIE |
| `source_ref` | text | idempotencja numeru dokumentu | tak | system | F9 | NIE |

Zakaz: zapis `charge.buy_amount` / `sell_amount` z adaptera; KSeF z ERP; surowy SQL do bazy klienta.

---

## 7. Extraction HITL (kind, bbox, enhance, drabina)

`extraction_draft` ISTNIEJE (`003`): `status`, `source_ref`, `input_text`, `payload` JSONB, `reviewed_by`, `reviewed_at`. **Brak kolumny `kind`.**  
Payload ISTNIEJE w Pydantic `ExtractionPayload` / `ExtractedChargeCandidate` (`backend/app/ai_transforms/extraction/schemas.py`). Docling `ocr_grade` — **brak w kodzie**. `layout_fingerprint` — funkcja parsera, nie kolumna.

### 7.1 `extraction_draft` — rozszerzenie kolumn

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `status` | enum `pending`/`accepted`/`rejected` | stan HITL | tak | HITL | M-20 | ISTNIEJE `extraction_draft.status` |
| `source_ref` | text | dokument źródłowy | tak | system | M-20 | ISTNIEJE `extraction_draft.source_ref` |
| `input_text` | text | tekst wejsciowy | tak | parser | M-20 | ISTNIEJE `extraction_draft.input_text` |
| `payload` | JSONB | kandydaci + unparsed | tak | extract | M-20 | ISTNIEJE `extraction_draft.payload` |
| `reviewed_by` | UUID nullable | kto recenzował | nie | HITL | M-20 | ISTNIEJE `extraction_draft.reviewed_by` |
| `reviewed_at` | timestamptz | kiedy | nie | HITL | M-20 | ISTNIEJE `extraction_draft.reviewed_at` |
| `draft_kind` | enum `rate_line` / `purchase_invoice` / `customer_rfq` / `shipment_document` / `party_document` / `carrier_quote` | ten sam split UI, inny kind | tak | system | F10 + X9 + O6 | NIE |
| `inbound_message_id` | UUID FK nullable | mail źródłowy | nie | system | F10 | NIE |
| `original_blob_ref` | text | oryginał zdjęcia/PDF | nie | upload | X9 | NIE |
| `enhanced_blob_ref` | text | wersja „skaner”; recenzja idzie stąd | nie | OpenCV | X9 | NIE |
| `reject_reason` | text | powód zbiorczego odrzucenia | nie | operator | X9 | NIE |
| `page_count` | int ≥ 1 | strony | nie | parser | X9 | NIE |

### 7.2 Payload `ExtractionPayload` (JSONB, nie osobna tabela)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `payload.source_ref` | text | echo źródła w payloadzie | tak | extract | M-20 | ISTNIEJE klucz JSONB `source_ref` |
| `payload.unparsed_regions` | text[] | region nierozpoznany (GLOSSARY) | tak (może pusta lista) | extract | M-20 | ISTNIEJE `unparsed_regions` |
| `payload.candidates` | lista | kandydaci | tak (może pusta) | extract | M-20 | ISTNIEJE `candidates` |
| `payload.parser_name` | text | który parser | nie | system | 0.9 | ISTNIEJE `parser_name` |
| `payload.parser_challenger` | text | challenger A/B | nie | system | 0.9 | ISTNIEJE `parser_challenger` |
| `payload.ab_delta_chars` | int | delta A/B (GLOSSARY) | nie | system | 0.9 | ISTNIEJE `ab_delta_chars` |
| `payload.layout_fingerprint` | text | `pdf` vs `text` | nie | parser | 0.9 | NIE w payloadzie (funkcja `layout_fingerprint` ISTNIEJE) |
| `payload.layout_grade` | text | ocena layout Docling | nie | Docling | X9 | NIE |
| `payload.ocr_grade` | text | ocena OCR | nie | Docling | X9 | NIE |
| `payload.mean_grade` | text | średnia ocena strony | nie | Docling | X9 | NIE |
| `payload.low_grade` | text | `poor`…`excellent`; `poor` → zrób zdjęcie ponownie | nie | Docling | X9 | NIE |

### 7.3 Kandydat / `ExtractedField` w `candidates[]`

Dziś tylko stawka. X9: dowolne pole (NIP, numer FV, data, kontener, waga, …). Kwota zostaje `amount_text` → Decimal **przy accept**, nie w JS.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `code` | text | kod opłaty / etykieta pola | tak (dla stawki) | extract | M-20 | ISTNIEJE `ExtractedChargeCandidate.code` |
| `amount_text` | text | kwota jako tekst | tak gdy pole kwotowe | extract / operator | M-20 | ISTNIEJE `amount_text` |
| `currency` | CHAR(3) | waluta | tak gdy kwota | extract | M-20 | ISTNIEJE `currency` |
| `note` | text | notatka kandydata | nie | extract | M-20 | ISTNIEJE `note` |
| `field_kind` | text | `charge` / `tax_id` / `invoice_ref` / `invoice_date` / `container_no` / `weight_kg` / … | tak | extract | X9 + F10 | NIE |
| `span_text` | text | fragment z OCR | nie | extract | X9 | NIE |
| `confidence` | Numeric 0–1 | pewność per pole | tak | extract | X9 | NIE (makieta UI ma, schemat nie) |
| `bbox_page` | int ≥ 1 | strona ramki | tak gdy bbox | extract | X9 | NIE |
| `bbox_x` | Numeric | x ramki | tak gdy bbox | extract | X9 | NIE |
| `bbox_y` | Numeric | y ramki | tak gdy bbox | extract | X9 | NIE |
| `bbox_w` | Numeric | szerokość | tak gdy bbox | extract | X9 | NIE |
| `bbox_h` | Numeric | wysokość | tak gdy bbox | extract | X9 | NIE |
| `operator_override` | bool | człowiek poprawił wartość; pewność modelu bez zmian | tak po edycji | operator | X9 | NIE |

### 7.4 `scan_enhance_run` — NOWA tabela (metadane OpenCV)

Oryginał zostaje. Zakaz GAN / inpaintingu tekstu.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `extraction_draft_id` | UUID FK | szkic | tak | system | X9 | NIE |
| `original_source_ref` | text | wejście (mail/skan/apka) | tak | system | X9 | NIE |
| `enhanced_source_ref` | text | wyjście „płaski skaner” | tak gdy enhance się udał | OpenCV | X9 | NIE |
| `capture_engine` | text | `ml_kit` / `visionkit` / `server` | tak | apka / serwer | X9 | NIE |
| `mlkit_mode` | enum `base_with_filter` / `full` | FULL nie na FV | nie | apka | X9 | NIE |
| `warp_applied` | bool | 4 rogi + perspective | tak | OpenCV | X9 | NIE |
| `deskew_applied` | bool | wyprostowanie | tak | OpenCV | X9 | NIE |
| `white_point_applied` | bool | biel papieru | tak | OpenCV | X9 | NIE |
| `output_mode` | enum `color` / `gray` / `bw` | kolor default FV; B/W CMR | tak | system | X9 | NIE |
| `dpi_out` | int | cel ~300; Lanczos, nie generator | nie | OpenCV | X9 | NIE |
| `quality_gate_passed` | bool | Laplace / prostokąt; false = zrób ponownie | tak | gate | X9 | NIE |
| `source_ref` | text | wersja pipeline | tak | system | X9 | NIE |

### 7.5 `invoice_match_candidate` — NOWA tabela (drabina SQL)

Score liczy SQL, nie model. **Nigdy auto-podpięcie.**

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `extraction_draft_id` | UUID FK | szkic FV kosztowej | tak | system | F10 | NIE |
| `shipment_id` | UUID FK nullable | kandydat zlecenia | nie | SQL | F10 | NIE |
| `charge_id` | UUID FK nullable | otwarte `charge.buy` bez FV | nie | SQL | F10 | NIE |
| `ladder_step` | enum `shipment_ref` / `identifiers` / `seller_tax_amount_date` / `mail_thread` / `lane_month` / `unassigned` | który szczebel | tak | SQL | F10 | NIE |
| `score` | Numeric 0–1 | waga szczebla; nie float JS | tak | SQL | F10 | NIE |
| `is_unique_hit` | bool | unikalne trafienie szczebla 1 | tak | SQL | F10 | NIE |
| `source_ref` | text | które sygnały | tak | SQL | F10 | NIE |

Sygnały szczebla `identifiers` (nie osobne kolumny, treść w `source_ref` / payload): kontener ISO, B/L, booking, PIN, nr SENT, płyta.

`inbound_message` ISTNIEJE (`from_address`, `subject`, `body_text`, `external_id`, `party_id`). Do `replied` i szczebla wątku:

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `rfc822_message_id` | text | Message-ID | nie | ingest | X7 + F10 | NIE |
| `in_reply_to` | text | In-Reply-To | nie | ingest | X7 | NIE |

---

## 8. Dokumenty sieci / szablon / QR

M-38 `shipment_document` ISTNIEJE: `document_kind` IN (`noted`,`attached`,`other`), `source_ref`, `shipment_id`. **Bez bajtów.** D9 dodaje blob + wymóg sieci. M-26 to `document_number` na `quotation` + token szablonu oferty, nie tabela layoutów.

### 8.1 `network_print_requirement` — NOWA tabela

Blokada wyjazdu jak C8: 409, odblokowanie = wydruk + `source_ref`.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `network_id` | UUID FK → `network` | która sieć drobnicowa | tak | operator | D9 | NIE |
| `party_role` | text | rola, dla której wymóg (np. carrier) | nie | operator | D9 | NIE |
| `document_kind` | text | etykieta sieci / CMR / list załadunkowy / … | tak | operator | D9 | NIE |
| `blocks_departure` | bool | brak wydruku → 409 | tak | operator | D9 | NIE |
| `source_ref` | text | pochodzenie reguły | tak | operator | D9 | NIE |

`network.code` / `network_member` — ISTNIEJE.

### 8.2 `document_template` — NOWA tabela

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `template_kind` | enum `own_label` / `network_label` / `cmr` / `cmr_groupage` / `hbl` / `mbl` / `carrier_order` / `loading_list` / `quotation` | rodzaj wydruku | tak | operator | D9 | NIE |
| `language` | text | język layoutu | tak | operator | D9 | NIE |
| `layout_ref` | text | wskazanie layoutu (dane, nie T-SQL SPEED) | tak | operator | D9 | NIE |
| `branding_ref` | text | branding tenanta | nie | operator | D9 | NIE |
| `output_kind` | enum `html_print` / `pdf` / `zpl` | U-print / PDF / Zebra | tak | operator | D9 | NIE |
| `source_ref` | text | pochodzenie | tak | operator | D9 | NIE |

### 8.3 `shipment_package` — NOWA tabela (segment QR)

QR: `tenant` + `shipment` + `package` + `document_kind`.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `shipment_id` | UUID FK | zlecenie | tak | operator | D2 + D9 | NIE |
| `package_code` | text | kod paczki/palety | tak | system / operator | D2 | NIE |
| `source_ref` | text | pochodzenie | tak | operator | D2 | NIE |

### 8.4 `shipment_document` — rozszerzenie

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `document_kind` | text | dziś `noted`/`attached`/`other` — D9 rozszerzy allowlistę | tak | operator / skan | M-38 | ISTNIEJE `shipment_document.document_kind` |
| `source_ref` | text | dziś wskazanie; D9 `scan://…` | tak | operator / skaner | M-38 | ISTNIEJE `shipment_document.source_ref` |
| `blob_ref` | text | bajty w storage tenanta | tak gdy skan/wydruk | system | D9 | NIE |
| `content_sha256` | text | dedup pliku+kind+shipment | tak gdy blob | system | D9 | NIE |
| `package_id` | UUID FK nullable | paczka z QR | nie | skan | D9 | NIE |
| `scan_match_kind` | enum `omni_qr` / `hitl` | nasz kod = zapis od razu; brak kodu = HITL | tak gdy skan | system | D9 | NIE |
| `barcode_payload` | text | surowy odczyt QR/kreskowego | nie | skaner | D9 | NIE |

Nasz QR odczytany → SQL jedno zlecenie → zapis bez LLM. Kolizja / obcy tenant = stop. Diff CMR vs zlecenie = X6, nie cichy overwrite.

---

## 9. Poczta (książka nadawcza)

### 9.1 `party` — rozszerzenie (domyślny kanał papieru)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `default_invoice_delivery_channel` | enum `electronic` / `paper_post` | ten klient zawsze papier vs elektronika | nie | operator | F11 | NIE |

### 9.2 `sales_invoice` — rozszerzenie (migracja `054`+`055`)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `invoice_kind` | enum `issued`/`noted`/`other` | rodzaj FV sprzedaży | tak | operator | M-40 | ISTNIEJE `sales_invoice.invoice_kind` |
| `invoice_ref` | text | numer FV Omni | tak | operator | M-40 | ISTNIEJE `sales_invoice.invoice_ref` |
| `ksef_ref` | text nullable | numer sesji/ref KSeF | nie | operator (wpis) | 97.0 | ISTNIEJE `sales_invoice.ksef_ref` |
| `ksef_noted_at` | timestamptz | kiedy odnotowano KSeF | nie | operator | 97.0 | ISTNIEJE `sales_invoice.ksef_noted_at` |
| `shipment_id` | UUID FK | zlecenie | tak | operator | M-40 | ISTNIEJE `sales_invoice.shipment_id` |
| `source_ref` | text | pochodzenie | tak | operator | M-40 | ISTNIEJE `sales_invoice.source_ref` |
| `delivery_channel` | enum `electronic` / `paper_post` | papier = książka PP; **nie** wyłącza KSeF | tak | operator / default z `party` | F11 | NIE |

`paper_post` bez `postal_dispatch` = kolejka „do nadania”, nie „wysłana”.

### 9.3 `postal_dispatch` — NOWA tabela

Jeden wiersz = jedna przesyłka. Klucz = `numer_nadania` (oficjalny token PP `numerNadania`; analogia do `ksef_ref`).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `sales_invoice_id` | UUID FK | FV papierowa | tak | operator / system | F11 | NIE |
| `party_id` | UUID FK | adresat | tak | system | F11 | NIE |
| `numer_nadania` | text | kod z nalepki; bez numeru nie ma wiersza | tak | EN API / skaner HID / wklejenie+checksum | F11 | NIE |
| `envelope_ref` | text | id koperty EN (`sendEnvelope`) | nie | EN SOAP | F11 | NIE |
| `epo_service_kind` | enum `none` / `simple` / `extended` | usługa EPO na przesyłce | tak | operator / EN | F11 | NIE |
| `dispatch_status` | text | nadana / w drodze / doręczona / kolejka | tak | REST śledzenia / operator | F11 | NIE |
| `source_ref` | text | `en://` / `scan://` / `manual://` | tak | system | F11 | NIE |

Idempotencja: ten sam `numer_nadania` w tenancie = ten sam wiersz.

### 9.4 `postal_tracking_event` — NOWA tabela

Upsert po `numer_nadania` + kod + czas. Zdarzenie kończące zatrzymuje poll.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `postal_dispatch_id` | UUID FK | przesyłka | tak | system | F11 | NIE |
| `event_code` | text | np. `P_D`, `P_UKEPO`, `finished` | tak | REST `checkmailex` | F11 | NIE |
| `occurred_at` | timestamptz | czas zdarzenia | tak | API | F11 | NIE |
| `is_terminal` | bool | kończy obsługę / poll | tak | API | F11 | NIE |
| `source_ref` | text | idempotentne wywołanie | tak | API | F11 | NIE |

Imienia **nie ma** w REST.

### 9.5 `postal_epo` — NOWA tabela (PII)

Tylko przy umowie EPO. Podpisu i biometrii nie logować. Nie w promptach.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `postal_dispatch_id` | UUID FK | przesyłka | tak | EN `getEPOStatus` | F11 | NIE |
| `recipient_name` | text | `osobaOdbierajaca` | nie | EPO XML | F11 | NIE |
| `delivery_subject` | text | `podmiotDoreczenia` (ADRESAT, UPOWAZNIONY_PRACOWNIK, …) | nie | EPO | F11 | NIE |
| `delivered_at` | timestamptz | data doręczenia EPO | nie | EPO | F11 | NIE |
| `bioepo_available` | bool | obraz podpisu istnieje u PP; **nie przechowujemy bajtów** | tak | EPO | F11 | NIE |
| `source_ref` | text | wywołanie EN | tak | API | F11 | NIE |

Papierowe ZPO bez EPO: skan na FV (§13n) po HITL; OCR nie zgaduje nazwiska jako faktu.

Koszt znaczka = `charge` + `source_ref` (cennik PP / FV PP), nie pole na `postal_dispatch`.

---

## 10. Faktury (sprzedaż ISTNIEJE, zakup NOWY) + lejek oferty

### 10.1 `purchase_invoice` — NOWA tabela

Nie wchodzi na zlecenie bez HITL accept. Dedup: KSeF **albo** (sprzedawca + numer + data).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `party_id` | UUID FK | sprzedawca | tak | HITL | F9 + F10 | NIE |
| `invoice_ref` | text | numer FV zakupu | tak | HITL / FA(3) | F10 | NIE |
| `invoice_date` | date | data FV | tak | HITL / XML | F10 | NIE |
| `net_amount` | Numeric(14,4) | netto | tak | HITL (nie LLM „na czysto”) | F10 | NIE |
| `gross_amount` | Numeric(14,4) | brutto | tak | HITL | F10 | NIE |
| `currency` | CHAR(3) | waluta obu kwot | tak | HITL | F10 | NIE |
| `ksef_ref` | text nullable | numer KSeF nabycia (Subject2) | nie | API KSeF 2.0 | F10 | NIE |
| `status` | enum `draft` / `accepted` / `unassigned` | po accept dopiero FK i ERP | tak | HITL | F10 | NIE |
| `inbound_message_id` | UUID FK nullable | mail | nie | system | F10 | NIE |
| `extraction_draft_id` | UUID FK | szkic kind=`purchase_invoice` | tak | system | F10 | NIE |
| `source_ref` | text | mail / `ksef://` / `scan://` | tak | system | F10 | NIE |

XML FA(3) = parser deterministyczny, nie LLM.

### 10.2 `purchase_invoice_allocation` — NOWA tabela

Jedna FV → wiele zleceń. Suma linii = kwota FV (**SQL**).

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `purchase_invoice_id` | UUID FK | FV kosztowa | tak | HITL | F10 | NIE |
| `shipment_id` | UUID FK | zlecenie | tak | HITL | F10 | NIE |
| `charge_id` | UUID FK nullable | które `charge.buy` | nie | HITL | F10 | NIE |
| `line_amount` | Numeric(14,4) | kwota alokacji | tak | HITL | F10 | NIE |
| `currency` | CHAR(3) | = waluta FV | tak | HITL | F10 | NIE |
| `source_ref` | text | accept | tak | HITL | F10 | NIE |

`quote_invoice_settlement` ISTNIEJE (para wycena + FV **sprzedaży**) — nie używać do FZ.

### 10.3 `quote_engagement` — NOWA tabela (lejek oferty)

Append-only. Czasy = SQL na znacznikach, nie Python/JS/LLM.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `quotation_id` | UUID FK → `quotation` | oferta | tak | system | X7 | NIE |
| `mail_draft_id` | UUID FK nullable | szkic/wysłanie | nie | system | X7 | NIE |
| `party_contact_id` | UUID FK nullable | odbiorca (zgoda na piksel) | nie | system | X7 | NIE |
| `event_kind` | enum `sent` / `delivered` / `email_opened` / `pdf_viewed` / `replied` / `converted` / `lost` | szczebel lejka | tak | system / HTTP / ingest | X7 | NIE |
| `occurred_at` | timestamptz | kiedy | tak | system | X7 | NIE |
| `certainty_kind` | enum `high` / `prefetch` / `human` | Apple MPP vs klik | tak | system | X7 | NIE |
| `source_ref` | text | Graph / mailto / `GET /q/{token}` | tak | system | X7 | NIE |

`quotation.document_number` — ISTNIEJE (unikalny per org gdy nie NULL).  
`mail_draft.status` / `to_address` — ISTNIEJE (`draft`/`sent`).  
Konwersja: `shipment.quotation_id` ISTNIEJE.

### 10.4 `quote_view_token` — NOWA tabela (hostowany PDF)

Załącznik nie trackuje. Główny sygnał = GET tokenu.

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `quotation_id` | UUID FK | która oferta | tak | system | X7 | NIE |
| `token_hash` | text | niezgadywalny token (hash w DB) | tak | system | X7 | NIE |
| `expires_at` | timestamptz | TTL = ważność oferty | tak | system | X7 | NIE |
| `last_viewed_at` | timestamptz | ostatni GET | nie | HTTP | X7 | NIE |
| `source_ref` | text | wystawienie tokenu | tak | system | X7 | NIE |

### 10.5 `party_contact` — rozszerzenie (zgoda na piksel)

| Pole | Typ | Znaczenie PL | Obowiązkowe | Źródło | Fala | Już w kodzie? |
|---|---|---|---|---|---|---|
| `name` | text | nazwa kontaktu | tak | operator | M-10 | ISTNIEJE `party_contact.name` |
| `email` | text | adres | nie | operator | M-10 | ISTNIEJE `party_contact.email` |
| `tracking_consent` | bool | zgoda na piksel HTML (osobna od zgody na mail; ePrivacy) | tak | operator / kontakt | X7 | NIE |

Bez zgody mail idzie **bez** piksela. Tracker trzeciej strony zakazany.

---

## Nowe tabele vs rozszerzenia

### NOWE (brak tabeli w modelach / alembic)

1. `relation_document_requirement`
2. `resource`
3. `trip`
4. `stop`
5. `position_event`
6. `telematics_connector`
7. `resource_telematics_link`
8. `exchange_message`
9. `entity_event`
10. `weather_observation`
11. `party_document`
12. `party_exchange_snapshot`
13. `monitoring_scheme`
14. `shipment_monitoring_filing`
15. `map_basemap`
16. `user_map_prefs`
17. `tenant_map_provider`
18. `erp_connector`
19. `erp_series_map`
20. `erp_export`
21. `scan_enhance_run`
22. `invoice_match_candidate`
23. `network_print_requirement`
24. `document_template`
25. `shipment_package`
26. `postal_dispatch`
27. `postal_tracking_event`
28. `postal_epo`
29. `purchase_invoice`
30. `purchase_invoice_allocation`
31. `quote_engagement`
32. `quote_view_token`
33. `party_lane_scorecard` (O5)
34. `party_role_assignment` (M10-2)
35. `prediction_ledger` (B0b/V1)
36. `plan_snapshot` (B0b)
37. `incoterm_responsibility` (I1)
38. `shipment_stakeholder` (I2)
39. `document_dispatch_rule` / `document_dispatch` (I3)
40. `booking_instruction` (I4)
41. `terminal_slot_connector` / `terminal_appointment` (T8)

### Rozszerzenie istniejącej tabeli (kolumny, których **nie ma** dziś)

| Tabela | Nowe pola | Uwaga kolizji |
|---|---|---|
| `organization_setting` | nowe **klucze** allowlisty (nie kolumny) | `setting_value` VARCHAR(64); sekrety odrzucone |
| `shipment` | `shipment_ref`, `is_waste` | status dziś tylko `draft` |
| `carrier_inquiry` | `quoted_amount`, `quoted_currency`, lane, `quoted_transit_days`, `sent_at` | dziś `draft` + zero kwot; Fala O |
| `channel_quote` | `transit_days` | O1; znaczki SQL nie kolumny |
| `network_member` | `party_id` | O0 |
| `charge` | `source_ref` | luka: myto i znaczek PP wymagają pochodzenia; **P0** |
| `extraction_draft` | `draft_kind`, `inbound_message_id`, `original_blob_ref`, `enhanced_blob_ref`, `reject_reason`, `page_count` | kind w kolumnie, bbox w JSONB |
| `extraction_draft.payload` | fingerprint, oceny Docling, bbox/confidence/`field_kind`/`operator_override` | kandydat dziś bez bbox |
| `inbound_message` | `rfc822_message_id`, `in_reply_to` | `external_id` już jest (Graph/IMAP) |
| `shipment_document` | `blob_ref`, `content_sha256`, `package_id`, `scan_match_kind`, `barcode_payload` | allowlista `document_kind` do rozszerzenia |
| `sales_invoice` | `delivery_channel` | `ksef_ref` już jest; papier ≠ wyłączenie KSeF |
| `party` | `default_invoice_delivery_channel` | nie mylić z `party_scorecard` |
| `party_contact` | `tracking_consent` | |
| `table_view` | `group_by` | O8; `party`/`country`/`thread`/`status`; tabela ISTNIEJE |
| `resource_telematics_link` | `observation_kind` | V5; dwa reżimy |
| `credit_review` | `suggested_text` | M14b; Decimal limitu wpisuje człowiek / SQL, nie LLM |

### Istnieje i **nie** dublować nową tabelą

`organization`, `app_user`, `organization_setting`, `shipment`, `shipment_leg`, `tracking_event`, `location` (lat/lng), `party`, `party_contact`, `party_scorecard`, `network`, `network_member`, `carrier_inquiry`, `charge`, `charge_code`, `rate_line`, `quotation` (`document_number`), `mail_draft`, `inbound_message`, `extraction_draft`, `shipment_document`, `sales_invoice`, `bookkeeping`, `quote_invoice_settlement`, `table_view`, `outbox_event`.

---

## Zakazy (żeby katalog nie spłynął w kod)

- Float na kwotach, współrzędnych, confidence, score, mycie.
- LLM liczący ETA, myto, VAT, sumę alokacji, czasy lejka.
- Poll floty na **zewnętrznym** GPS poza 3 dniami roboczymi; sekrety w logach i w `organization_setting`.
- Auto-accept extractu, auto-link FV do zlecenia, **auto-decyzja** kredytowa / HR (szkic + S11 wolno).
- GAN / dopisywanie tekstu na skanie.
- Scraping czatu giełd i profili Trans.eu.
- Druga kolumna marży obok `charge`.
- `tracking_event` jako GPS.

## Tally

- **324+** wiersze pól w katalogu (50 ISTNIEJE w kodzie; dopiski O/M10/B0 w kartach fal).
- **32** tabele wizji wieczornej + **4** z pinu O/B0/M10 (`party_lane_scorecard`, `party_role_assignment`, `prediction_ledger`, `plan_snapshot`).
- Powtórzenia typu `source_ref` są zamierzone: to to samo HC na różnych obiektach, nie drugi magazyn.

Plan tnie tę kartę do jednego plastra. WIP=1.

---

## Pin 2026-09-08c — EXP1 (nie dubluj tu 80 kolumn)

Pełna lista nazw: [karty-pol-fala-exp.md](karty-pol-fala-exp.md). Przy `/plan-modul` obiektu wciągnij wiersze EXP1 do tej karty (typ + obowiązkowe + fala). Nie zgaduj kolumn w kodzie z tej sekcji.

Klucz korpo na `shipment` (jeszcze NIE w kodzie): `sold_to_party_id`, `bill_to_party_id`, `ship_to_party_id`, `notify_party_id`, `named_place`, `incoterms_version`, `actual_haulier_party_id`, `customer_po`.  
CI: `customer_contract` tylko ciphertext.  
G2.23: `kreptd_licence_no`, `kreptd_checked_at`.
