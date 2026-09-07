# Karty pól — Fala T (warstwa wykonawcza) — SZKIC do `/plan-modul`

**Status:** szkic wejściowy. Finalne nazwy kolumn ustala Plan modułu wg `docs/GLOSSARY.md`; każda tabela dostaje `organization_id` + RLS + test izolacji; kwoty `Decimal` z walutą; współrzędne bez float; zero pól „na zapas" — karta wskazuje maksimum, Plan tnie do jednego plastra.  
**Wzorce:** ekrany interLAN SPEED (zlecenie drogowe/morskie/kontener), model API Qargo (Order/Stop/Trip/Resource/Task), pola z PDF rozmowy (43 obiekty — `docs/_source/benchmark/chatgpt-pdf-digest-1/2/3.md`).

## Zasada „wpisz raz, zapisz na stałe"

Każdy formularz spełnia cztery mechanizmy trwałości (wszystkie już mają fundament w kodzie):

| Mechanizm | Fundament | Zastosowanie na kartach |
|---|---|---|
| Słowniki per tenant | wzorzec `charge_code` (M-06), `port` (M-05), `party` (M-10) | miejsca, teksty ustaleń, rodzaje opakowań, typy kosztów |
| Szablony | M-03 `organization_setting` (prefiks/szablon numeru), M-26 dokument | szablony zleceń, teksty ustaleń, charge templates (Fala P) |
| Wartości domyślne per tenant | M-03 (`default_currency`) | domyślna waluta, tabela kursu, termin płatności, profil auta |
| Saved views | `table_view` RLS + ViewManager (0.6) | widoki list per użytkownik; współdzielenie = ULEPSZ (Fala X) |

Pola typu „wybierz z listy" zawsze wskazują słownik (FK), nigdy luźny string — nieznany token = odrzut (wzorzec `resolve` z M-05).

## T1 — `stop` (punkt operacyjny)

Wzorzec: grid „Miejsca załadunku i wyładunku" SPEED + routing portów ZM + Stop/Stop group z Qargo.

| Pole (szkic) | Typ | Słownik / walidacja | Uwagi |
|---|---|---|---|
| shipment_id / trip_id | FK | — | stop żyje przy zleceniu; trip podpina stopy wielu zleceń (T2) |
| kind | enum | `loading` / `unloading` / `customs` / `ferry` / `terminal` / `depot` / `other` | SPEED: ZA/WY + typy pośrednie; Qargo: collection/delivery/other |
| sequence_no | int | unikat w ramach zlecenia | Lp z grida SPEED |
| location_id | FK → `location`/`port` (M-05) | resolve tokenu, odrzut nieznanych | miejsce ze słownika, nie luźny adres |
| planned_date / planned_time_from / planned_time_to | date/time | okno czasowe | SPEED: Data plan + Godz plan; FIX = okno zwężone |
| actual_arrival_at / actual_departure_at | timestamptz | — | podstawa plan vs wykonanie |
| status | enum | `pending` / `at_stop` / `completed` / `failed` | Qargo: AT_STOP/COMPLETED w visibility events |
| weight_kg / quantity / packaging_code | Decimal / int / FK słownik opakowań | ≥ 0 | SPEED: Waga, Ilość, j.w. |
| reference | text | — | nr ref punktu (awizacja, booking) |
| notes_for_driver | text | — | SPEED: info dla kierowcy |

`stop_group` (Qargo) = opcjonalne grupowanie stopów wykonywanych razem — rozstrzygnąć w Planie, czy tabela, czy kolumna grupująca.

## T2 — `trip` + `resource`

Wzorzec: Trip/Resource z Qargo (trip = jednostka kosztowo-wykonawcza; stopy z wielu orders) + sekcja Przewoźnik/Sam./Nacz./Kier. I-II ze SPEED.

`trip`:

| Pole (szkic) | Typ | Słownik / walidacja | Uwagi |
|---|---|---|---|
| trip_no | text | numeracja z szablonu M-03 | |
| status | enum | `draft` / `planned` / `in_transit` / `completed` / `cancelled` | przejście `planned → in_transit` zamraża snapshot kosztu (expected; Fala P) |
| vehicle_id / trailer_id | FK → resource | ważności dokumentów sprawdzane przy przypisaniu | SPEED: nr inw. + nr rej. |
| driver_id / driver2_id | FK → resource | dwóch kierowców (MC: multi-manning) | SPEED: Kier. I / Kier. II + tel. |
| subcontractor_party_id | FK → `party` (M-10) | — | trip własny albo podwykonawcy |
| planned_distance_km / actual_distance_km | Decimal | ≥ 0 | SPEED: Odl. wg zlec. / Odległość |
| route_label | text | — | SPEED: „GDYNIA (PL) - BŁONIE (PL)" |

`resource` (jedna tabela z `kind` albo trzy — rozstrzyga Plan; Qargo trzyma vehicle/driver/trailer jako Resource):

| Pole (szkic) | Typ | Uwagi |
|---|---|---|
| kind | enum `vehicle` / `driver` / `trailer` | |
| name / registration_no / inventory_no | text | SPEED: nr rej. + nr inw. |
| vehicle_profile | FK słownik | SPEED: „Profil samochodu: HERE" — profil routingowy |
| capacity_kg / capacity_ldm / capacity_m3 | Decimal | walidacje select&drop (T6) |
| adr_certified / reefer / tail_lift | bool | dopasowanie wymagań zlecenia |
| document_expiries | tabela zależna (rodzaj + data ważności) | SPEED: kontrola ważności dokumentów kierowcy/pojazdu/przewoźnika przy planowaniu |
| phone / driver_card_no | text | kierowca |

## T3 — `container` (obiekt kontenera)

Wzorzec: ekran „Edycja danych kontenera" SPEED (najbogatszy publiczny formularz) + zakładka Kontener na zleceniu drogowym + Ładunek/Kontenery na ZM.

| Pole (szkic) | Typ | Słownik / walidacja | Uwagi |
|---|---|---|---|
| container_no | text | ISO 6346 + cyfra kontrolna | SPEED pokazuje „Numer kontenera jest poprawny" — walidacja na wejściu |
| container_type | FK słownik (`40'HC`, `20'DV`…) + TEU wyliczone | słownik typów ISO | |
| shipment_id / shipment_leg_id | FK | — | kontener na zleceniu morskim; podpinany też do podzlecenia drogowego (T4) |
| carrier_party_id | FK → `party` | — | operator/armator (SPEED: MSC SWITZERLAND) |
| vessel_name / voyage_no | text | — | SPEED: Statek / Nr rejsu |
| pol_port_id / pod_port_id / destination_city | FK → `port` / text | — | |
| hbl_no / mbl_no / booking_no | text | — | |
| seal_no_1 / seal_no_2 / seal_no_3 | text | — | SPEED: 3 plomby |
| pin_code | text (szyfrowane w spoczynku) | HC-05 | PIN odbioru — sekret operacyjny |
| pickup_terminal_id / return_terminal_id | FK → `terminal` (M-05 4.2) | — | terminal pobrania pełnego / złożenia pustego |
| pickup_date / return_date / gate_in_date / delivery_date / unload_date | date | — | komplet dat SPEED |
| demurrage_free_days / detention_free_days / mixed_dd_days | int | ≥ 0 | SPEED: Demurrage / Detention / MIX D/D |
| cargo_description / quantity / packaging_code / weight_kg / volume_m3 | text / Decimal / FK | — | SPEED: Ładunek, Ilość, Waga, Obj |
| reefer / temp_min / temp_max / needs_external_power | bool / Decimal | temp tylko gdy reefer | SPEED: Chłodniczy, Temp. min/max, zasilanie |
| vgm_weight_kg / tare_weight_kg | Decimal | — | SPEED: Waga VGM / TARA |
| ref_1…ref_5 / remarks | text | — | SPEED: Ref 1–5 + Uwagi |
| container_release_party_id | FK → `party` | — | ZM SPEED: „Zwolnienie kontenera dla" |

Cut-offy (CARGO / DOK / VGM — ekran ZM „Dane dod.") — rozstrzygnąć w Planie: na kontenerze czy na nodze morskiej.

## T4 — zlecenie główne / podzlecenia

Wzorzec: pole „Zlecenie główne" (SPEED, zakładka Inne) + Rentowność ZM („Przychód/Koszt z podzleceń").

| Pole (szkic) | Typ | Uwagi |
|---|---|---|
| parent_shipment_id | FK → `shipment`, nullable | podzlecenie wskazuje główne; NULL = zlecenie samodzielne |
| relation_kind | enum `drayage` / `oncarriage` / `leg_subcontract` / `other` | dowóz/odwóz kontenera = najczęstszy przypadek SPEED |

Rentowność główne+podzlecenia liczy SQL (widok), nie Python — HC-07; marża zostaje w `charge` (HC-02).

## T5 — `task` (zadanie z reguł)

Wzorzec: Task engine Qargo (warunki: route / goods / service level / transport service / vehicle category / customer / department; wykonanie asynchroniczne).

| Pole (szkic) | Typ | Uwagi |
|---|---|---|
| template_id | FK → `task_template` | szablon = dane (nazwa, warunki JSONB, przypisanie, deadline offset) |
| shipment_id / trip_id / stop_id | FK (jeden z) | kontekst zadania |
| assignee_kind / assignee_id | enum + FK | użytkownik / dział |
| due_at / status | timestamptz / enum `open`/`done`/`skipped` | done przez szynę decyzji (M-71) tam, gdzie zadanie = decyzja |

Warunki szablonu ewaluowane w SQL na kolumnach (wzorzec `applies_when` z M-18) — nie parser AST, nie LLM. Async po outboxie (M-02) dopiero, gdy jest konsument.

## T7 — kurs wg daty (polityka kursu na opłacie)

Wzorzec: SPEED Fracht („Tabela kursów wg: daty załadunku, −1 dzień, NBP-A/B, Śr.") + Kalkulacje ZM („Kurs wg daty ETD, Tabela NBP/MIL, Typ kursu Średni").

| Pole (szkic) | Typ | Słownik | Uwagi |
|---|---|---|---|
| fx_rate_basis | enum | `etd` / `loading_date` / `unloading_date` / `invoice_date` | która data zlecenia rządzi kursem |
| fx_rate_offset_days | int (domyślnie 0 / −1) | — | „−1 dzień roboczy" — NBP D-1, art. 31a ustawy o VAT |
| fx_rate_table | enum | `nbp_a` / `nbp_b` | odczyt z `nbp_rate` (M-23); żadnego mnożenia w Pythonie |

Domyślna polityka per tenant w M-03; nadpisanie per zlecenie/opłata. Przeliczenie wykonuje SQL przy fakturowaniu — LLM i JS nie liczą (HC-02).

## T8 — slot na każdym terminalu (capability, nie gwarancja)

| Pole (szkic) | Typ | Uwagi |
|---|---|---|
| `terminal_id` | FK → `terminal` | każdy terminal M-05 ma wiersz |
| `mode` | enum | `api` / `email_hitl` / `portal_task` / `unsupported` |
| `appointment.window` | timestamptz range | `requested` / `confirmed` / `rejected` |
| `source_ref` | text | umowa API albo `email:` / `portal:` |

P0 API = umowa (Baltic Hub TO_VERIFY). Brak API ≠ Selenium. Semafor UI: zielony/żółty/szary. Audyt [incoterms-booking-customs-ux.md](incoterms-booking-customs-ux.md).

## Poza Falą T (zapowiedź kart)

Planning board (T6) to widoki na `stop`/`trip` — pola pochodne, osobna karta UI przy Planie. Fale D/P/X/F/C/V dostaną karty pól analogicznie przed swoim `/plan-modul` (drobnica: przesyłka/paczka/linia/awizacja; pricing: rate card/charge template; finanse: skonto/rezerwa/delegacja).
