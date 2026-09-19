# Słownik domenowy PL / EN

Ten plik pilnuje **naszych** nazw. Leftover (VISION D.7 / PLAN AI5.0): ta sama
etykieta KPI (OTD / OTIF) może mieć inną formułę u HHL, klienta, przewoźnika
i wieży — z właścicielem i źródłem prawdy. AI nie wymyśla wzoru. Nie zgaduj
kolumn. Nie 468.0.

| PL | EN (kod) | Uwagi |
|---|---|---|
| stawka | rate_line | niemutowalna, source_ref |
| opłata / charge | charge / shipment_charge | jedyne miejsce prawdy o marży; buy+sell na jednym wierszu |
| kupno | buy | kwota zakupu na `charge` |
| sprzedaż | sell | kwota sprzedaży na `charge` |
| marża | margin | sell − buy, ta sama waluta; zapis: `margin()`; GET lista: SQL; nie kolumna magazynu |
| kod opłaty | charge_code | katalog M-06; typowany token, nie luźny string |
| alias kodu opłaty | charge_code alias | synonim w katalogu tenanta |
| kod towarowy | commodity_code | katalog M-09; 70.0 FK na RFQ/wycenie; nie luźna nazwa |
| towar niebezpieczny | dangerous_good | katalog M-52; 122.0 FK na RFQ/wycenie; 192.0 HITL tunel ADR + SG; nie LLM |
| numer UN | un_number | 4 cyfry na `dangerous_good`; prefiks UN zbędny |
| klasa IMDG | imdg_class | allowlista 1–9 z podziałem (2.1, 4.1, …); nie packing group |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| port załadunku | origin_port_id | POL na `quotation`; FK do `port` |
| port wyładunku | destination_port_id | POD na `quotation`; FK do `port` |
| zlecenie | shipment | 90.0 tabela z wyceny z `party_id`; nie tracking |
| zlecenie główne | parent_shipment_id | T4 HITL 210.0 FK na `shipment` + `relation_kind`; nie SQL marży |
| numer zlecenia | shipment_ref | D9b HITL 204.0 twardy numer na zleceniu; nie QR; nie PDF; nie generator GD |
| śledzenie | tracking | 91.0 `tracking_event` na zleceniu; nie AIS; nie mapa |
| wyjątek operacyjny | operational_exception | 93.0 tabela na zleceniu; nie AIS; nie mapa; nie `party_charge_override` |
| wieża | watchtower | 94.0 wyjątki + pending S11 + leniwy panel mapy; 116.0 odczyt `mail_draft`; 124.0 liczniki tablicy; nie leaflet; nie AIS; nie czat; nie łańcuch V6 |
| impact wieży | tower_impact | V6 HITL 198.0 etap łańcucha + status umowy; bez sla_clause = „brak danych umowy”; nie scoring osoby; nie EBITDA |
| bliźniak | twin_mark | W1 HITL 199.0 / 440.0 FK do twin_kind; nie fizyka; nie plan_snapshot |
| rodzaj bliźniaka | twin_kind | AI1.4 HITL otwarty słownik kind_code; nie CHECK; nie twin_mark |
| źródło danych | data_source | AI5.0 HITL source_code + license_label + rights_scope; nie live ingest; nie CHECK listy |
| brama ingest | ingest_gate_mark | AI5.0 leftover HITL truth|owner|exception; nie live ingest |
| cecha modelu | model_feature_mark | AI5.1 HITL numeric|categorical|derived; nie live train; nie feature store |
| narracja CFO | cfo_narrative_mark | AI7.1 HITL anomaly|story|summary; nie silnik narracji; nie druga marża |
| definicja KPI | kpi_definition_mark | AI5.0 leftover HITL otd|otif|custom; nie wzór z modelu; nie OTIF% |
| poziom autonomii | autonomy_level | AI1.4 HITL otwarty słownik level_code; nie CHECK; nie FK klienta |
| klucz alokacji kosztów | allocation_key | AI7.0 HITL otwarty słownik key_code; nie SQL alokacji; nie druga marża; nie cost_allocation_mark |
| kategoria kosztu | cost_category_mark | AI7.0 HITL 6 kategorii PDF + other; nie SQL; nie TCM; nie cost_allocation_mark |
| poziom alokacji kosztów | allocation_level | AI7.0 HITL otwarty słownik level_code; nie CHECK 12; nie SQL; nie TCM |
| węzeł skutku biznesowego | impact_node_mark | AI6.0 HITL 8 węzłów kaskady + other; nie SQL grafu; nie EBITDA; nie tower_impact |
| krawędź skutku biznesowego | impact_edge_mark | AI6.0 HITL para from_kind/to_kind; nie FK węzeł; nie SQL grafu; nie EBITDA |
| etykieta art. 50 | article50_mark | AI9.0 HITL generated|exempt|human|other; nie U-art50 UI; nie scoring |
| sala kryzysowa | war_room_mark | W2 HITL 200.0 rodzaj incydentu; nie N8; nie drugi czat; nie T8 API |
| sala operacyjna | ops_room_mark | BR7.0 HITL warstwa działająca (shift/board/escalation); nie N8; nie widok sklejony |
| warstwa liczona linii | line_impact_layer_mark | BR7.1 HITL scored/forecast/actual; nie SQL EBITDA; nie plant live |
| ticket produktu | product_ticket_mark | Plat-HD HITL report/triage/owner_ok; nie CAPA; nie auto-naprawa; nie operator_notice |
| rejestr ryzyka | risk_register_mark | AI9.2 HITL open/mitigated/accepted; nie scoring osoby; nie L3 silnik |
| program zgodności | compliance_program_mark | AI9.2 leftover HITL draft/review/signed/exempt; nie PDF bytes; nie U-art50 |
| automation bias | automation_bias_mark | AI9.1 HITL confirm/delay/review; nie ui-04 przebudowa; nie auto-accept |
| pewność per pole (pasmo) | field_confidence_mark | AI9.1 leftover HITL green/yellow/orange/hold; nie float; nie przebudowa splitu |
| brama L3 | l3_gate_mark | AI8.2 HITL sot/owner/exception/rollback/blast; nie L3 write; nie mutacja autonomy_level |
| ticket produktu | product_ticket_mark | Plat-HD HITL report/triage/owner_ok; nie CAPA; nie auto-naprawa |
| krawędź pamięci | memory_edge | W3 HITL 201.0 rodzaj krawędzi; nie RAG; nie graf na entity_event |
| pytanie zarządu | executive_mark | W4 HITL 202.0 rodzaj pytania; nie suma LLM; nie narracja SQL |
| oś rankingu | rank_mark | W5 HITL 203.0 oś zakupu; nie auto-award; nie N szkiców |
| dokument zlecenia | shipment_document | 92.0 tabela na zleceniu; nie bajty; nie PDF; nie HBL |
| komunikat EDI | edi_message | 95.0 tabela na zleceniu; 32.0 leftover tablica kanału; nie parser; nie live HTTP |
| faktura sprzedaży | sales_invoice | 96.0 tabela na zleceniu; 97.0 `ksef_ref` wpisany; nie live HTTP; nie druga marża |
| rozliczenie wyceny z fakturą | quote_invoice_settlement | 98.0 tabela pary wycena+faktura; nie kwota; nie druga marża |
| bank i płatności | bank_payment | 99.0 tabela pary faktura+rachunek; nie kwota; nie SEPA |
| koszt pieniądza | money_cost | 100.0 tabela pary płatność+kurs NBP; nie kwota; nie odsetki |
| różnica kursowa | fx_difference | 101.0 tabela pary wycena+kurs NBP; nie kwota; nie przeliczenie |
| przepływ | cash_flow | 102.0 tabela pary wycena+płatność; nie kwota; nie odejmowanie |
| koszt obsługi klienta | cost_to_serve | 103.0 tabela pary SOP+wycena; nie kwota; nie suma |
| księgowość | bookkeeping | 104.0 tabela pary opłata+faktura; nie kwota; nie JPK |
| zbiorcza faktura | collective_invoice | 105.0 tabela pary faktura+dodatkowe zlecenie; nie kwota; nie płatność paczką |
| transport drogowy | road_transport | 41.0 tablica `location` lądowa; 108.0 odcinek `shipment_leg` road; nie TMS; nie GPS |
| punkt operacyjny | stop | T1; ZA/WY na zleceniu; miejsce ze słownika; 213.0 opcjonalny `stop_group_code`; 215.0 opcjonalny `notes_for_driver`; 247.0 opcjonalny `weight_kg`; 248.0 opcjonalny `quantity`; 249.0 opcjonalny `packaging_code`; 250.0 opcjonalny `seal_in`; 251.0 opcjonalny `seal_out`; 252.0 opcjonalny `appointment_ref`; 253.0 opcjonalny `waiting_free_minutes`; 254.0 opcjonalny `waiting_started_at`; 255.0 opcjonalny `pod_quality`; nie mapa |
| zasób floty | resource | T2; pojazd / kierowca / naczepa; 259.0 trasa `/fleet`; nie trip; nie GPS |
| przejazd | trip | T2; status + opcjonalny zasób; 212.0 opcjonalny `driver2_id`; 214.0 opcjonalny `route_label`; 256.0 opcjonalny `planned_distance_km`; 257.0 opcjonalny `actual_distance_km`; 258.0 opcjonalny `subcontractor_party_id`; 167.0 snapshot `expected_buy`; nie liczenie km; nie wariancja |
| tablica planowania | planning board | 261.0 `/planning` leniwy overlay `trip`; nie 4 widoki; nie leaflet |
| snapshot kosztu kupna | expected_buy | P5 freeze Decimal na `trip` przy `in_transit`/`completed`; nie marża; nie SQL na `charge` |
| kontener | container | T3; ISO 6346 + iso_size_type; 216.0–218.0 trzy plomby; 219.0 `vessel_name`; 220.0 `voyage_no`; 221.0 `remarks`; 222.0 `cargo_description`; 223.0 `packaging_code`; 224.0 `ref_1`; 225.0 `ref_2`; 226.0 `ref_3`; 227.0 `ref_4`; 228.0 `ref_5`; 229.0 `reefer`; 230.0 `pickup_terminal`; 231.0 `return_terminal`; 232.0 `bl_kind` (nie HBL); 233.0 `free_time_origin_h` (nie odliczanie); 234.0 `free_time_dest_h` (nie odliczanie); 566.0 `demurrage_free_days` (dni HITL, nie countdown); 567.0 `detention_free_days` (dni HITL, nie countdown); 568.0 `mixed_dd_days` (dni HITL, nie countdown); 235.0 `si_cutoff_at` (nie live HTTP); 236.0 `ams_cutoff_at` (nie live HTTP); 237.0 `cy_cutoff_at` (nie live HTTP); 238.0 `cfs_cutoff_at` (nie live HTTP); 239.0 `vgm_kg` / `vgm_method` / `vgm_cutoff_at` (nie kalkulator, nie live HTTP); 569.0 `tare_kg` (tara HITL Decimal, nie kalkulator, nie VGM); 570.0 `pin_code` (PIN odbioru HITL tekst, nie live terminal, nie ciphertext); 571.0 `payload_kg` (ładowność HITL Decimal, nie kalkulator, nie quantity); 572.0 `teu` (TEU HITL Decimal, nie kalkulator z typu ISO); 573.0 `quantity` (ilość HITL Integer, nie stop.quantity); 574.0 `weight_kg` (waga HITL Decimal, nie stop.weight_kg, nie VGM); 575.0 `volume_m3` (objętość HITL Decimal, nie kalkulator CBM, nie waga); 576.0 `pickup_date` (data odbioru HITL date, nie cutoff, nie countdown); 577.0 `return_date` (data zwrotu HITL date, nie cutoff, nie countdown); 578.0 `gate_in_date` (data wjazdu HITL date, nie cutoff, nie countdown); 240.0 `last_survey_at` (nie live HTTP); 241.0 `booking_no` (nie S21, nie live HTTP); 242.0 `carrier_party_id` (FK party, nie PIN, nie live HTTP); 243.0 `shipment_leg_id` (FK odcinka, nie PIN, nie live HTTP); nie temperatura; nie FK terminalu; nie PIN |
| odcinek | shipment_leg | 108.0 `road` · 109.0 `rail` · 110.0 `china_rail` · 111.0 `ocean_lcl` · 154.0 `air` na zleceniu; nie mapa; nie ETA |
| kolej intermodalna | intermodal_rail | 42.0 tablica `port` z flagą `rail`; 109.0 odcinek `shipment_leg` rail; nie wagon; nie CIM |
| kolej z Chin | china_rail | 43.0 tablica `port` CN z flagą `rail`; 110.0 odcinek `shipment_leg` china_rail; nie korytarz; nie HTTP |
| drobnica morska | ocean_lcl | 44.0 tablica `port` z `is_seaport`; 111.0 odcinek `shipment_leg` ocean_lcl; nie tabela LCL; nie CFS |
| linia drobnicy | groupage_line | 155.0 katalog linii LTL: `cutoff_local`, `transit_days`, `operating_dows`, dwa `location`; nie OR hubów; nie WMS |
| znacznik dyspozytora drobnicy | groupage_dispatcher_mark | BR3.2 HITL katalog; leftover silnik hubów / konsolidacja |
| paczka na zleceniu | shipment_package | 156.0 sztuka na `shipment`: `package_status`, skan QR Omni, `stop` z trasy; nie WMS; nie auto-link |
| awizacja doku | dock_appointment | 157.0 okno TIME na `stop` w magazynie (`postal_zone`/`address`); nie WMS; nie T8 |
| pobranie COD | cod_instruction | 158.0 znacznik na `shipment` bez kwoty; nie rozliczenie F; nie POD portu |
| cennik drobnicy | groupage_tariff | 159.0 próg `chargeable_weight` na strefie; Decimal; nie silnik P1; nie FSC |
| konosament LCL | ocean_bill | 160.0 HBL/MBL na `shipment`; nie PDF; nie booking; nie druga tabela LCL |
| saldo palet | pallet_balance | 161.0 Chep/LPR na `party`; integer sztuk; nie giełda; nie depozyt |
| szablon wydruku | document_template | 162.0 layout jako dane; nie `quotation_print_template`; nie PDF |
| karta stawek | rate_card | 163.0 `applies_when` jako dane + Decimal; 205.0 równość GET matching; nie silnik WHEN/IF; nie `rate_line` |
| szablon opłat | charge_template | 164.0 kolekcja `charge_code` + daty; 206.0 exclusion daterange; nie `charge` |
| szablon zadania | task_template | T5 HITL 263.0 kod + `applies_when`; 264.0 outbox `task_template_saved`; nie instancja `task`; nie matching |
| indeks paliwowy | fuel_index | 165.0 katalog FSC/BAF/CAF obok `nbp_rate`; nie przeliczenie na `charge` |
| dopłata lokalna | local_charge | 166.0 THC/ISPS/seal/amendment + Decimal; 207.0 opcjonalny `port_unlocode`; 208.0 opcjonalny `iso_size_type`; nie warning; nie `port_surcharge` |
| lotniczy | air | 154.0 odcinek `shipment_leg` air; 209.0 opcjonalny `hawb_no`/`mawb_no`; lotnisko = `port` z `airport`; nie pula IATA |
| reklamacja ładunku | cargo_claim | 113.0 tabela na zleceniu; 191.0 HITL OS&D + terminy CMR; nie kwota; nie silnik 7/21/365 |
| oszustwo | fraud_flag | 114.0 tabela na kontrahencie; nie scoring osoby; nie kwota |
| sankcje | sanctions | 45.0 tablica aktywnych `party`; 89.0 sprawdzenie `sanctions_list_ref` na karcie; nie auto-match; nie live lista |
| RODO | gdpr | 46.0 tablica `app_user` email; 107.0 wniosek `gdpr_request`; nie DPIA |
| wniosek RODO | gdpr_request | 107.0 tabela access/erasure; erasure = tombstone konta; nie DELETE `app_user` |
| copilot AI | ai_copilot | 47.0 tablica `extraction_draft` pending; 76.0 `mail_draft` obok extract; 81.0 świadomy mailto; 116.0 wieża czyta szkice; 118.0 SOP `blocks_auto` na `/ai`; nie czat; nie auto-send |
| szkic maila | mail_draft | 76.0 tabela wychodzącego szkicu; accept przez S11; 81.0 status `sent` + `to_address`; nie inbound |
| obserwowalność | observability | 48.0 tablica `fetchHealth`; nie OTel; nie k6 |
| jakość ekstrakcji | extraction_quality | 49.0 tablica `unparsed_regions`; nie scoring; nie tabela QA |
| wdrożenie tenanta | tenant_rollout | 50.0 tablica `default_currency`; nie tabela rollout; nie upsert |
| oś dziesiętna kwoty | money_axis | 52.0 siatka integer/ułamek/ISO na `<Money/>`; nie float |
| gęstość zagęszczona | table_density_condensed | 53.0 trzeci tryb tylko na gridzie `rate_line`; nie globalnie |
| pin Radix shadcn | shadcn_radix_base | 54.0 `components.json` `base: radix`; nie Base UI |
| komunikat UI | ui_message | 55.0 klucz i18n w katalogu `pl`; nie drugi język |
| ścieżka E2E axe | e2e_axe_route | 56.0 Playwright + axe na trasie; nie live accept |
| arkusz druku | print_sheet | 57.0 `@media print` chowa chrome; nie PDF |
| tenant | organization | organization_id wszędzie |
| ustawienie tenanta | organization_setting | 3.0 waluta; 71.0 prefiks i token szablonu; nie sekret; nie licznik |
| token sesji | session token | JWT HS256; claims `sub` + `org` |
| token odświeżający | refresh_token | rotacja; RLS; nie access JWT |
| skrót hasła | password_hash | argon2id; nigdy plaintext w API |
| pochodzenie | source_ref | obowiązkowe |
| zastąpiona przez | superseded_by | stary wiersz wskazuje nowy; kwoty się nie nadpisuje |
| szkic ekstrakcji | extraction_draft | HITL przed zapisem domeny; `draft_kind` `rate_line`\|`carrier_quote`\|`tender_rfp`; 140.0 accept quote→`channel_quote`; 531.0 plan leftover→inquiry `answered`; 447.0 PATCH; 448.0 revision; 449.0 `extract_path`; 503.0 `history` |
| ścieżka ekstrakcji | extract_path | `text` albo `image`; etykieta, nie live vision |
| ramka kandydata | bbox_text | dana na kandydacie; nie float; nie rysunek PDF |
| pewność kandydata | confidence_text | dana na kandydacie; nie float; nie próg auto-accept |
| brama accept zbiorczy | bulk_accept_confidence | 501.0 Decimal 0,70 na `confidence_text` przy ≥2 kandydatach; jeden wiersz = HITL bez bramki; nie auto-accept |
| prompt ekstrakcji (katalog) | extraction_prompt_mark | 502.0 HITL extract\|system\|other; prompt jako dana; nie wiring LLM |
| szkic RFP | tender_rfp | G2.9b `draft_kind`; accept → `tender_rfp_intake`; nie zapis z LLM |
| syntetyk ewaluacji | synthetic document | fixture extract/eval (`synth://`); zero PDF klienta |
| stub Presidio | InstructorPresidioStub | tylko ścieżka instructor; nie każdy endpoint |
| region nierozpoznany | unparsed_region | zawsze w payloadzie ekstrakcji |
| odcisk układu | layout_fingerprint | pdf vs text przed parserem |
| delta A/B parsera | ab_delta_chars | różnica długości tekstu A vs B (0.9) |
| kurs NBP | nbp_rate | D-1 roboczy; 16.0 odczyt przy wycenie; nie drugi katalog; nie mnożenie kwoty |
| polityka kursu | fx_rate_basis | T7 HITL 211.0 w `organization_setting`; offset 0/−1; tabela nbp_a/nbp_b; nie mnożenie |
| ryzyko oferty | offer_risk | 17.0 odczyt; 87.0 wskazanie recenzji na wycenie; nie scoring |
| negocjacja oferty | offer_negotiation | 18.0 odczyt; 85.0 wskazanie `channel_quote` na wycenie; nie nowa kwota; nie spread w JS |
| dokument oferty | offer_document | 19.0 podgląd; 72.0 `document_number` + druk 57.0; nie PDF; nie send |
| wycena wsadowa | quotation_batch | 20.0 wiele kodów na jednej lane; nie CSV; nie nowa tabela |
| zapytanie od klienta | customer_inquiry | 21.0 ślad wycen per party; nie tabela RFQ; nie IMAP |
| zapytanie ofertowe | customer_rfq | 67.0 obiekt; 68.0 wycena; 70.0 `commodity_code_id`; nie kwota na RFQ |
| wykrywanie akceptacji | offer_acceptance | 22.0 pending; 86.0 decyzja S11 na `quotation`; nie HITL accept; nie IMAP |
| zapytanie do armatora | carrier_inquiry | 83.0 obiekt buy do `network_member`; Fala O: batch, statusy `queued`/`sent`/`answered`, lane; N5 data ciszy `no_reply_after`; **533.0** O8 group_by party/kraj/wątek(lane)/status + `table_view`; 23.0 ślad `channel_quote`; nie RFQ; nie live HTTP; nie nowy czat |
| porównanie odpowiedzi | response_comparison | 84.0 zapis `charge` (buy kanał, sell wycena); 24.0 zestawienie na POL/POD; nie odejmuj w JS |
| integracja pocztowa | mail_integration | 25.0 tablica znanych adresów na `/mail`; 64.0 dopina `inbound_message`; nie IMAP |
| wiadomość przychodząca | inbound_message | 64.0 tabela per tenant; 66.0 treść → extract HITL; 78.0/80.0 ingest `graph://` / `imap://` + `external_id`; 79.0 zdarzenie outbox; nie live skrzynka; nie send; nie blob |
| zdarzenie outbox | outbox_event | 79.0 tabela per tenant; 264.0 kind `task_template_saved` obok `inbound_message_saved`; nie Temporal; nie konsument |
| klient poczty | mail_client | 26.0 `mailto:` z `party_contact.email`; 81.0 dispatch zaakceptowanego szkicu; nie dodatek Office; nie Graph HTTP |
| powiadomienie operatora | operator_notice | 27.0 tablica pending; 75.0 inbox; 123.0 filtr kind; nie auto-INSERT; nie wysyłka |
| narzut | markup | kaskada — Python mały zbiór (DECISIONS) |
| pieniądze | money | para `amount` + `currency`; nigdy float |
| kwota | amount | `Decimal` / tekst dziesiętny, skala Numeric(14,4) |
| waluta | currency | ISO 4217 CHAR(3), nierozerwalnie z kwotą |
| port | port | katalog M-05; UN/LOCODE per tenant |
| kod UN/LOCODE | unlocode | 5 znaków, np. PLGDY |
| alias portu | port alias | synonim na wierszu `port`; seed z improved-un-locodes |
| lokalizacja | location | 4.1; kind unlocode / postal_zone / address |
| strefa taryfowa | location_zone_member | 4.1; zakresy kodów pocztowych per tenant |
| terminal | terminal | 4.2; osobna tabela, nie `location.kind` |
| kod ISPS | isps_code | identyfikator obiektu portowego; unikat per tenant gdy nie NULL |
| opłata portowa warunkowa | port_surcharge | M-18; katalog extra; 69.0 matching `applies_when` w SQL; nie `charge.margin` |
| oferta z kanału | channel_quote | M-19; katalog oferty armatora per POL/POD; O1 `transit_days`; nie live HTTP; nie `rate_line` |
| czas tranzytu | transit_days | dni kalendarzowe na ofercie kanału; znaczek najszybszy TT liczy SQL; nie float |
| karta lane | party_lane_scorecard | M-13 per POL/POD; SQL-refresh; podpowiedź z pól; nie scoring osoby; nie LLM |
| zdarzenie obiektu | entity_event | B0a append-only (`inquiry_queued` 244.0 z API / `inquiry_sent` 245.0 z API / `quote_recorded` 246.0 z API); nie Temporal |
| przypisanie roli | party_role_assignment | 132.0; wiele ról na jednym `party`; nie osobny kontrahent na rolę |
| JDG | is_sole_trader | 132.0; kredyt tylko HITL recenzją |
| kontrahent nadrzędny | parent_party_id | 132.0; grupa / oddział; FK tenanta |
| ledger predykcji | prediction_ledger | B0b/V1; 193.0 HITL przedział; 446.0 zdejmuje wpis CRPS/MAE; metryka = interval_score |
| ledger podpowiedzi | suggestion_ledger | AI1.0 HITL przedział + reaction + changed_to; nie zapis LLM; nie CRPS liczone |
| ledger wyniku | outcome_ledger | AI1.1 HITL actual_value Decimal; UUID podpowiedzi jako dana |
| wynik przedziału | interval_score | AI2.0 MAE+CRPS liczone w SQL ze złączenia ledgerów; nie wpis |
| wynik wersji | version_score | AI2.1 średnie MAE/CRPS per model_version; nie auto-champion |
| wynik okna wersji | version_window | AI2.1 średnie MAE/CRPS per model_version i dzień UTC; nie detektor |
| wynik okna wersji | version_window | AI2.1 leftover: średnie MAE/CRPS per model_version i dzień UTC z created_at; nie detektor |
| rodzaj wyniku | outcome_kind | AI1.4 HITL otwarty słownik kind_code; FK z outcome_ledger (442.0) |
| przebieg what-if | counterfactual_run | AI1.2 HITL etykiety + AI4.1 FK do `plan_snapshot` i widok `what_if_replay`; nie silnik liczb; nie kwota |
| ledger oszczędności | benefit_ledger | AI1.3 HITL method_label + hours_saved + saved_amount Decimal; nie druga marża; nie SQL z charge |
| rodzaj podpowiedzi | suggestion_kind | AI1.4 HITL otwarty słownik kind_code; nie CHECK; nie kolumna ledgeru |
| migawka planu | plan_snapshot | B0b; 265.0 HITL wersja planu; 452.0 FK złożone RESTRICT; nie silnik; nie kółka |
| operator terminalu | operator_name / operator_party_id | tekst zostaje; FK nullable do `party` od 5.0 |
| kontrahent | party | katalog M-10; jeden podmiot, wiele ról |
| identyfikator podatkowy | tax_id | NIP / VAT krajowy; `resolve` po tokenie |
| numer VAT UE | vat_eu | unikat per tenant; lookup VIES nie zapisuje sam |
| numer EORI | eori | unikat per tenant; 131.0; nie live celny |
| numer DUNS | duns | unikat per tenant; 9 cyfr; 131.0 |
| REGON | regon | opcjonalny |
| KRS | krs | opcjonalny |
| role kontrahenta | party roles | `customer` `vendor` `agent` `carrier` `shipper` `consignee` `notify` |
| kontakt kontrahenta | party_contact | bez portalu w 5.0 |
| rachunek kontrahenta | party_bank_account | IBAN; `whitelist_status` z lookupu |
| domena mailowa kontrahenta | party_email_domain | katalog; matcher maili = M-11 |
| dopasowanie maila | resolve_email | M-11; domena z adresu → `party`; 65.0 też na `inbound_message`; nie IMAP |
| wyjątek stawki kontrahenta | party_charge_override | katalog uzgodnień; nie silnik wyceny / nie marża |
| profil armatora | carrier_profile | 1:1 z `party`; adapter tylko jako dane |
| sieć spedycyjna | network | katalog M-12; token kodu (`wca`, `fiata`, …); kopia per tenant; nie portal |
| kod sieci | network code | snake 2–32; `resolve` po kodzie albo aliasie |
| członek sieci | network_member | 82.0 ręczny agent w `network` tenanta; O0 `party_id` FK tenanta; O7 filtr `country_code` z `party` (141.0 UI · 532.0 API); nie portal |
| kod kraju kontrahenta | country_code | ISO 3166-1 alpha-2 na `party`; filtr listy agentów O7; nie druga kolumna na `network_member` |
| karta wyników kontrahenta | party_scorecard | M-13; 10.0 snapshot globalny; 120.0 odczyt decyzji oferty; lane = `party_lane_scorecard` (O5); nie scoring osoby; nie silnik RFQ |
| recenzja kredytowa | credit_review | M-14; decyzja operatora per `party`+dzień; 88.0 `bureau_attachment_ref`; M14b szkic sugestii; zapis limitu tylko S11; LLM nie liczy limitu |
| decyzja operatora | operator_decision | 74.0 szyna pending/accept/reject; 77.0 `lock_version`; 121.0 `changed`; nie HITL extract; nie send |
| tablica finansowa | finance_board | M-15; 15.0 odczyt marży/NBP/limitu/recenzji; 106.0 też FV; 117.0 narracja po SQL; LLM nie liczy |
| wskaźnik odpowiedzi | response_rate | 0–1 Numeric na karcie; NULL = nieznany |
| mediana czasu odpowiedzi | median_response_hours | godziny Numeric na karcie |
| pozycja cenowa | price_position | 0–1 Numeric na karcie partii w 10.0; per lane = `party_lane_scorecard` (O5) |
| procedura operacyjna klienta | customer_sop | M-16; 11.0 katalog; 73.0 `blocks_auto`; nie send; nie generator zadań |
| numer WPI | wpi_number | World Port Index (NGA Pub 150) na `port` |
| wielkość portu | harbor_size | WPI: Very Small / Small / Medium / Large |
| typ portu | harbor_type | WPI, słownik NGA |
| schronienie | shelter | WPI: Excellent / Good / Fair / Poor / None |
| głębokość toru | channel_depth_m | WPI, metry, Numeric |
| głębokość nabrzeża | cargo_pier_depth_m | WPI, metry, Numeric |
| Incoterms | incoterm | 11 reguł ICC 2020 jako enum danych; nie cytat oficjalnego tekstu ICC |
| macierz obowiązków | incoterm_responsibility | I1; 11 × import/export; seed ops Omni; override tenanta = nowy wiersz |
| strona handlu | trade_side | `import` = klient Omni jest kupującym; `export` = sprzedawcą |
| strona zlecenia | shipment_stakeholder | I2; rola + `party_id`; 409 na wysyłkę bez party |
| reguła adresata dokumentów | document_dispatch_rule | I3; trade_side×incoterm×document_kind → recipient_role; nie send |
| wysyłka dokumentów odprawy | document_dispatch | I3 leftover; N× `mail_draft` + `shipment_document`; send po S11; nie auto-send |
| instrukcja bookingu | booking_instruction | I4; scope + target z macierzy; `suggested` → accept człowieka |
| wymiana kontaktów | contact_exchange | zakres I4; DAP import: origin_agent + klient; nie booking ocean |
| rodzaj obserwacji GPS | observation_kind | V5; `omni_telematic` = flota w umowie pakietu; `external_api` = 3 dni robocze bez trip |
| konektor telematyki | telematics_connector | V5 HITL 197.0 reżim + dostawca; nie live GPS; nie sekrety |
| konektor ERP | erp_connector | F9 HITL 268.0 kod + kind `optima` + source_ref; nie live SOAP; nie sekrety |
| konektor slotu | terminal_slot_connector | T8 HITL 269.0 mode + godziny N4 + source_ref; nie booking; nie confirmed z formularza; nie gwarancja |
| konektor IdP | idp_connector | S53 HITL 270.0 kod + provider `auth0` + source_ref; nie login; nie live HTTP; nie sekrety |
| konektor giełdy | exchange_connector | S55 HITL 271.0 + BR5.2 473.0 kind P0 trans_eu/timocom/teleroute/transporeon/other + source_ref; nie live HTTP; nie SPA; nie sekrety |
| przepływ WMS | wms_flow_mark | BR1.0 HITL 474.0 receipt/location/pick/ship/count/other + source_ref; nie live WMS; nie qty; nie RFID |
| RFID magazyn | rfid_mark | BR1.1 HITL 475.0 reader/gate/tag/other + source_ref; nie live poll; nie EPC; nie FK bin |
| zapas finansowy | inventory_finance_mark | BR1.2 HITL 476.0 valuation/aging/release/other + source_ref; nie wycena SQL; nie kwota; nie FK |
| zabezpieczenie na towarze | inventory_collateral_mark | BR1.3 HITL 477.0 pledge/lien/hold/other + source_ref; nie FK pozycji; nie live zastaw |
| konektor widoczności | visibility_connector | CT7 HITL 275.0/294.0 kod + kind `p44`\|`fourkites`\|`shippeo` + source_ref; nie live HTTP; nie sekrety; nie AIS |
| zamówienie zakupu | purchase_order | CT1 HITL 276.0 nagłówek `po_code` + opcjonalny `plant_label` + source_ref; nie shipment |
| znacznik plant PO | po_plant_mark | EXP3.0b HITL plant\|batch\|sku\|other; nie live EDI; nie auto shipment |
| znacznik SKU PO | po_sku_mark | EXP3.0c HITL sku\|gtin\|customer_sku\|other; nie live EDI; nie auto shipment |
| znacznik batch PO | po_batch_mark | EXP3.0d HITL batch\|lot\|serial\|other; nie live EDI; nie auto shipment |
| znacznik segregacji UN | un_segregation_mark | EXP0.9 HITL tunnel\|segregation\|compat\|other; nie solver OR |
| znacznik dual ledger | dual_ledger_mark | EXP0.10 HITL ops\|finance\|tax\|other; nie druga marża |
| linia zamówienia zakupu | po_line | CT1 HITL 277.0 `line_code` + FK nagłówka + `sku_code` + `qty` Decimal + `uom_code` + etykiety; nie kwota |
| awizo wysyłki | asn | CT1 HITL 278.0 `asn_code` + FK nagłówka + etykiety; nie live EDI 856; nie auto shipment |
| przewodnik routingu | routing_guide | CT4 HITL 279.0 `guide_code` + etykiety; nie 409 egzekucja; nie mapa |
| tryb egzekucji przewodnika | routing_guide_enforcement | CT4 leftover HITL 285.0 `mark_code` + kind record_only\|block_409; nie żywy 409 |
| znacznik OTIF | otif_mark | CT3 HITL 280.0 `mark_code` + `scope_kind` pickup\|delivery\|sku; nie OTIF%; nie scoring SQL; definicja per strona = `kpi_definition_mark` (**526.0**) |
| tryb dopasowania przewodnika | routing_guide_match | CT4 HITL 288.0 kind guide_code_only\|lane_label\|mode_label; nie silnik |
| znacznik współpracy 3 stron | collaboration_mark | CT11 HITL 284.0 `mark_code` + role shipper\|carrier\|consignee; nie wspólny SELECT |
| znacznik audytu frachtu | freight_audit_mark | CT10 HITL 283.0 `mark_code` + kind expected_vs_invoice\|expected_vs_charge; nie SQL vs charge |
| znacznik dopasowania FV | invoice_match_mark | F10 HITL 550.0 `mark_code` + kind candidate\|rank\|allocate\|other; nie ranking SQL |
| znacznik alokacji FV | invoice_alloc_mark | F10 HITL 551.0 `mark_code` + kind line\|header\|batch\|other; nie allocation z kwotą |
| znacznik książki PP | postal_dispatch_mark | F11 HITL 552.0 `mark_code` + kind en\|uss\|epo\|other; nie live PP |
| znacznik CAPA | capa_mark | CT12 HITL 282.0 `mark_code` + kind capa\|eight_d\|recurrence; nie workflow |
| konektor SAP/Oracle | sap_connector | CT6 HITL 281.0 kod + kind `sap`\|`oracle`; nie live SOAP; nie sekrety |
| awizacja terminalu | terminal_appointment | T8; requested/confirmed/rejected; `source_ref` |
| kalendarz organizacji | organization_calendar | U4; dni robocze; grace GPS |
| przeniesienie pól | field_carry_forward | U1; oferta→zlecenie; nie cichy overwrite |
| reguła checklisty dokumentów | document_checklist_rule | U5; incoterm×strona×mode → rodzaj + blocks_dispatch |
| przesyłka | consignment | N1; 260.0 tabela na shipment; LTL/LCL=N; nie paczka; nie FTL unique |
| podłoga marży | margin_floor | N6; HITL Decimal DONE 527.0; leftover 409/S11 |
| intencja klonu zlecenia | shipment_clone_mark | N9; HITL DONE 528.0; leftover copy/U1 / similar SQL |
| przekazanie zmiany SBAR | handover_sbar_mark | N11; HITL DONE 529.0; leftover T6 bind |
| notatka przekazania SBAR | handover_note | N11 leftover; HITL DONE 543.0; leftover T6 bind · N8 |
| gotowość przejazdu do FV | trip_bill_mark | N2; HITL DONE 530.0; leftover SQL trips_to_bill · F1 live |
| ETA fizyczne | eta_physical | V2 HITL 194.0 na `stop`; GPS/korek leftover; nie jedyny znacznik |
| ETA prawne | eta_legal | V2 HITL 194.0 na `stop`; zakaz jazdy/tacho leftover |
| obserwacja pogody | weather_observation | V2 HITL 195.0; Open-Meteo/geometria leftover; nie ETA |
| zegar D&D | free_time_clock | V3 HITL 196.0 rodzaj + free_days; nie countdown; nie charge |
| blank sailing | blank_sailing_mark | V3 HITL 565.0 blank\|congestion\|gate; nie predykcja; nie N3 |
| umowa klienta | customer_contract | CI9 HITL 272.0 nagłówek; 273.0 opaque present/absent, nie szyfr; leftover `wrapped_dek`; nie super-admin |
| znacznik KEK | tenant_contract_kek | CI9 HITL 274.0 wrap_kind `password`/`kms`; nie klucz; nie materiał; 273.0 nadal nie szyfr |
| klauzula SLA | sla_clause | CI1 HITL 313.0 na `customer_contract`; próg jako tekst; leftover kara SQL / ciphertext |
| prognoza spóźnienia | delay_forecast | CI4 HITL 314.0; horizon_hours + p_late Decimal; nie wróżba punktowa; nie GPS |
| wynik interwencji | intervention_outcome | CI7 HITL katalog; leftover saved SQL |
| lead CRM | crm_lead | G1 HITL katalog; leftover szansa/activity |
| okazja CRM | crm_opportunity | BR6.0 HITL katalog; leftover activity / pipeline |
| aktywność CRM | crm_activity | BR6.0 leftover HITL katalog; nie silnik lejka |
| etap CRM | crm_pipeline_mark | BR6.0 leftover HITL katalog etapu; nie silnik lejka |
| dedup CRM | crm_dedup_mark | BR6.0 leftover HITL stance dedup; nie merge SQL |
| link CRM | crm_link_mark | BR6.0 leftover HITL stance powiązania; nie FK UUID |
| award załadowcy | shipper_award_mark | BR6.2 leftover HITL stance go/hold/no_award; nie Alpega |
| bind sprzedaży | sales_bind_mark | BR6.1 leftover HITL stance wiązania korytarza; nie HubSpot |
| bind załadowcy | shipper_bind_mark | BR6.2 leftover HITL stance wiązania tender|party; nie Alpega |
| korytarz sprzedażowy | sales_lane | BR6.1 HITL katalog; leftover UN/LOCODE / wolumen |
| tryb przetargu załadowcy | shipper_tender_mark | BR6.2 HITL katalog; leftover rundy / like-for-like |
| znacznik kampanii | campaign_mark | BR6.5 HITL katalog; leftover atrybucja live / lejek X7 |
| zdarzenie pozycji | position_event | BR2.0 HITL katalog; leftover współrzędne / poll |
| urządzenie telematyczne | telematics_device | BR2.1 HITL katalog; leftover parowanie / poll |
| zgoda na śledzenie | tracking_consent | BR2.2 HITL katalog; leftover kolumna na `party_contact` |
| checklista LC | lc_checklist | G3 HITL katalog; leftover bank/due |
| szkic NCTS | ncts_draft | G4 HITL katalog; leftover PUESC/plomby |
| znacznik OOG | oog_mark | G5 HITL katalog; leftover wymiary/cert |
| znacznik kolejności załadunku | load_order_mark | BR3.1 HITL katalog; leftover solver OR / wymiary Decimal |
| znacznik tacho w planie | tacho_plan_mark | BR3.3 HITL katalog; leftover live DDD / solver godzin |
| znacznik rezerwacji promu | ferry_booking_mark | BR4.0 HITL katalog; leftover live bilet / solver art. 9 |
| znacznik zezwolenia OOG | oog_permit_mark | BR4.1 HITL katalog; leftover wymiary Decimal / live zezwolenie |
| znacznik planu załadunku | load_plan_mark | G6 HITL katalog; leftover solver OR / osie / tunel ADR |
| znacznik planu trasy | route_plan_mark | BR3.0 HITL katalog; leftover Valhalla / VRP / km |
| znacznik CMMS | cmms_mark | G7 HITL katalog; leftover work_order / DTC V5 / kara kierowcy |
| znacznik legal hold | legal_hold_mark | G8 HITL katalog; leftover eIDAS crypto / wipe / F1 |
| znacznik spółki | company_mark | G10 HITL katalog; leftover company_id FK / drugi tenant |
| znacznik bonded | bonded_mark | G11 HITL katalog; leftover procedura / WMS e-com |
| schemat składania | filing_scheme_mark | G12 HITL katalog; leftover filer / deadline / SENT-UE |
| mapa EDI | edi_map_mark | G13 HITL katalog; leftover parser / silent write |
| dossier AEO | aeo_dossier_mark | G14 HITL katalog; leftover party_document / scoring |
| opcja naprawy | remediation_option | CI6 HITL 315.0; kind rebook/wait/claim/other; leftover kwota / S11 |
| scenariusz skutku | impact_scenario | CI6 HITL 316.0; chain_label tekst; nie EBITDA SQL; nie tower_impact |
| powiadomienie klauzuli | clause_notice | CI3 HITL 317.0; clause_label tekst; nie 409; nie auto-kara |
| znacznik kalibracji | calibration_mark | CI7 HITL 318.0; sample_ready ready\|pending; nie MAE SQL |
| playbook naprawy | repair_playbook | CI8 HITL 319.0; stance contain\|reroute\|claim\|other; nie auto-send S11 |
| znacznik wycieku | spend_mark | CI2 HITL 320.0; leakage invoice\|clause\|other; nie SQL FV vs charge |
| znacznik kary | penalty_mark | CI5 HITL 321.0; breach otif\|delay\|damage\|other; nie kara SQL |
| przetarg | tender | G2.0 nagłówek sell/buy; nie P6 `tender_quote`; nie loty |
| partia przetargu | tender_lot | G2.1 kod partii na `tender`; nie korytarz; nie kwota |
| korytarz przetargu | tender_lane | G2.2 para UN/LOCODE na `tender_lot`; nie runda; nie kwota |
| runda przetargu | tender_round | G2.3 numer rundy na `tender`; nie data room; nie kwota |
| pokój danych | tender_data_room | G2.4 NDA na `tender`; nie extract; nie bajty; nie kwota |
| komórka matrycy | tender_matrix_cell | G2.5 kwota Decimal z P na `tender`; nie LLM; nie druga marża |
| playbook przetargu | tender_playbook | G2.6 twierdzenie + `source_ref` na `tender`; nie extract RFP |
| wynik przetargu | tender_win_loss | G2.7 win/loss + `source_ref` na `tender`; nie extract RFP; nie four-eyes |
| członek konsorcjum | tender_consortium_member | G2.8 fotel na `tender` + `party`; nie extract RFP; nie TED |
| przyjęcie RFP | tender_rfp_intake | G2.9 HITL na `tender`; nie auto-award; nie zapis z LLM |
| prospekt przetargu | tender_prospect | G2.10 HITL outreach na `tender` + `party`; nie scrape; nie bid/no-bid |
| postawa udziału | tender_bid_stance | G2.11 HITL bid/no-bid na `tender`; nie win/loss; nie auto-award |
| przegląd nagrody | tender_award_review | G2.12 HITL cztery oczy na `tender`; nie auto-award; nie szyna A/Z/O |
| ogłoszenie TED | tender_ted_notice | G2.13 HITL numer TED na `tender`; nie scrape; nie live HTTP |
| znacznik śladu | tender_carbon_mark | G2.14 HITL declared/exempt na `tender`; nie kg; nie kalkulator |
| wzorzec korytarza | lane_pattern | G2.19 HITL para UN/LOCODE; nie km; nie circle_sim; nie `tender_lane` |
| oferta przetargowa kupna | tender_quote | P6 ważność + limit orderów; nie auto-award; nie obiekt `tender` |
| kółko | circle_sim | G2.20 HITL kod + para unload/load; AI4.2 widok `circle_sim_pair` unload↔load; nie generator 500k; nie km |
| km ładowny | lane_km | G2.21 HITL ładowny/pusty/dolot Decimal; nie Haversine; nie `trip`; nie `circle_sim` |
| KREPTD | kreptd | G2.23; GITD/ITD; oficjalne API |
| licencja KREPTD | kreptd_licence | G2.23 HITL numer licencji na `party`; nie scrape; nie Citizen API |
| schemat monitoringu | monitoring_scheme | C7 HITL katalog per tenant; nie zgłoszenie SENT; nie wymyślony klon |
| dokument kontrahenta | party_document | C8 HITL rodzaj na `party`; nie 409; nie extract |
| metodologia CO₂ | carbon_method | C5 HITL GLEC/GHG + wersja; nie kg; nie kalkulator |
| skonto | cash_discount | F2 HITL kind na `sales_invoice`; nie kwota; nie CAMT |
| licencja transportowa | transport_licence | party_document; KREPTD |
| sold-to | sold_to_party_id | EXP1; korpo |
| bill-to | bill_to_party_id | EXP1 |
| ship-to | ship_to_party_id | EXP1 |
| haulier faktyczny | actual_haulier_party_id | ≠ booked; double-broker |
| miejsce nazwane | named_place | Incoterms; 409 bez DAP/DDP |
| znacznik miejsca nazwanego | named_place_mark | EXP0.6 HITL named_place+2020\|2010; nie cytat ICC |
| znacznik stance slotu | slot_guarantee_mark | EXP0.3 HITL capability\|non_guarantee\|other; nie live T8 |
| znacznik warunku frachtu | freight_term_mark | EXP1 HITL prepaid\|collect\|third_party\|other; nie kolumna shipment |
| znacznik referencji PO klienta | customer_po_mark | EXP1 HITL customer_po\|release\|call_off\|other; nie purchase_order CT1 |
| znacznik centrum zysku/kosztu | profit_center_mark | EXP1 HITL profit\|cost\|project\|other; nie kolumna shipment |
| znacznik protokolu high-value | high_value_mark | EXP1 HITL high_value\|protocol\|other; nie kolumna shipment |
| znacznik warunków płatności | payment_terms_mark | EXP1 HITL net\|prepaid\|other; nie kolumna shipment |
| znacznik kodu języka | language_code_mark | EXP1 HITL pl\|en\|de\|other; nie kolumna shipment |
| znacznik roli przewoznika | haulier_role_mark | EXP1 HITL booked\|actual\|other; nie FK party |
| znacznik diversion | diversion_mark | EXP1 HITL diversion\|reroute\|other; nie FK shipment |
| znacznik spot/contract | spot_contract_mark | EXP1 HITL spot\|contract\|other; nie FK quotation |
| znacznik bid decision | bid_decision_mark | EXP1 HITL go\|no_go\|hold\|other; nie kolumna quotation |
| znacznik waluty wyceny | quote_currency_mark | EXP1 HITL account\|pay\|other; nie kolumna quotation |
| znacznik ważności wyceny | quote_validity_mark | EXP1 HITL open\|revised\|superseded\|other; nie kolumna quotation |
| fabryka demo | demo_sim | Demo-1; nie GBOX klienta |
| zakłócenie demo | demo_disruption | korki/wypadki fixture |
| zużycie platformy | platform_usage_daily | Admin-P; agregat; nie cross-tenant SELECT |
| tenant demo | demo_tenant | izolacja RLS; wipe USUN |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

