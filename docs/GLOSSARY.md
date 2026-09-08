# Słownik domenowy PL / EN

| PL | EN (kod) | Uwagi |
|---|---|---|
| stawka | rate_line | niemutowalna, source_ref |
| opłata / charge | charge / shipment_charge | jedyne miejsce prawdy o marży; buy+sell na jednym wierszu |
| kupno | buy | kwota zakupu na `charge` |
| sprzedaż | sell | kwota sprzedaży na `charge` |
| marża | margin | sell − buy, ta sama waluta; tylko funkcja `margin()` |
| kod opłaty | charge_code | katalog M-06; typowany token, nie luźny string |
| alias kodu opłaty | charge_code alias | synonim w katalogu tenanta |
| kod towarowy | commodity_code | katalog M-09; 70.0 FK na RFQ/wycenie; nie luźna nazwa |
| towar niebezpieczny | dangerous_good | katalog M-52; 122.0 FK na RFQ/wycenie; token UN czterema cyframi; nie LLM |
| numer UN | un_number | 4 cyfry na `dangerous_good`; prefiks UN zbędny |
| klasa IMDG | imdg_class | allowlista 1–9 z podziałem (2.1, 4.1, …); nie packing group |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| port załadunku | origin_port_id | POL na `quotation`; FK do `port` |
| port wyładunku | destination_port_id | POD na `quotation`; FK do `port` |
| zlecenie | shipment | 90.0 tabela z wyceny z `party_id`; nie tracking |
| śledzenie | tracking | 91.0 `tracking_event` na zleceniu; nie AIS; nie mapa |
| wyjątek operacyjny | operational_exception | 93.0 tabela na zleceniu; nie AIS; nie mapa; nie `party_charge_override` |
| wieża | watchtower | 94.0 wyjątki + pending S11 + leniwy panel mapy; 116.0 odczyt `mail_draft`; 124.0 liczniki tablicy; nie leaflet; nie AIS; nie czat |
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
| punkt operacyjny | stop | T1; ZA/WY na zleceniu; miejsce ze słownika; nie mapa |
| zasób floty | resource | T2; pojazd / kierowca / naczepa; nie trip |
| przejazd | trip | T2; status + opcjonalny zasób; 167.0 snapshot `expected_buy`; nie km; nie wariancja |
| snapshot kosztu kupna | expected_buy | P5 freeze Decimal na `trip` przy `in_transit`/`completed`; nie marża; nie SQL na `charge` |
| kontener | container | T3; ISO 6346 + iso_size_type; nie VGM |
| odcinek | shipment_leg | 108.0 `road` · 109.0 `rail` · 110.0 `china_rail` · 111.0 `ocean_lcl` · 154.0 `air` na zleceniu; nie mapa; nie ETA |
| kolej intermodalna | intermodal_rail | 42.0 tablica `port` z flagą `rail`; 109.0 odcinek `shipment_leg` rail; nie wagon; nie CIM |
| kolej z Chin | china_rail | 43.0 tablica `port` CN z flagą `rail`; 110.0 odcinek `shipment_leg` china_rail; nie korytarz; nie HTTP |
| drobnica morska | ocean_lcl | 44.0 tablica `port` z `is_seaport`; 111.0 odcinek `shipment_leg` ocean_lcl; nie tabela LCL; nie CFS |
| linia drobnicy | groupage_line | 155.0 katalog linii LTL: `cutoff_local`, `transit_days`, `operating_dows`, dwa `location`; nie OR hubów; nie WMS |
| paczka na zleceniu | shipment_package | 156.0 sztuka na `shipment`: `package_status`, skan QR Omni, `stop` z trasy; nie WMS; nie auto-link |
| awizacja doku | dock_appointment | 157.0 okno TIME na `stop` w magazynie (`postal_zone`/`address`); nie WMS; nie T8 |
| pobranie COD | cod_instruction | 158.0 znacznik na `shipment` bez kwoty; nie rozliczenie F; nie POD portu |
| cennik drobnicy | groupage_tariff | 159.0 próg `chargeable_weight` na strefie; Decimal; nie silnik P1; nie FSC |
| konosament LCL | ocean_bill | 160.0 HBL/MBL na `shipment`; nie PDF; nie booking; nie druga tabela LCL |
| saldo palet | pallet_balance | 161.0 Chep/LPR na `party`; integer sztuk; nie giełda; nie depozyt |
| szablon wydruku | document_template | 162.0 layout jako dane; nie `quotation_print_template`; nie PDF |
| karta stawek | rate_card | 163.0 `applies_when` jako dane + Decimal; nie silnik WHEN/IF; nie `rate_line` |
| szablon opłat | charge_template | 164.0 kolekcja `charge_code` + daty jako dane; nie exclusion; nie `charge` |
| indeks paliwowy | fuel_index | 165.0 katalog FSC/BAF/CAF obok `nbp_rate`; nie przeliczenie na `charge` |
| dopłata lokalna | local_charge | 166.0 THC/ISPS/seal/amendment jako dane + Decimal; nie warning; nie `port_surcharge` |
| lotniczy | air | 154.0 odcinek `shipment_leg` air; lotnisko = `port` z `airport` w `function_flags`; nie HAWB; nie IATA |
| reklamacja ładunku | cargo_claim | 113.0 tabela na zleceniu; nie kwota; nie scoring |
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
| szkic ekstrakcji | extraction_draft | HITL przed zapisem domeny |
| syntetyk ewaluacji | synthetic document | fixture extract/eval (`synth://`); zero PDF klienta |
| stub Presidio | InstructorPresidioStub | tylko ścieżka instructor; nie każdy endpoint |
| region nierozpoznany | unparsed_region | zawsze w payloadzie ekstrakcji |
| odcisk układu | layout_fingerprint | pdf vs text przed parserem |
| delta A/B parsera | ab_delta_chars | różnica długości tekstu A vs B (0.9) |
| kurs NBP | nbp_rate | D-1 roboczy; 16.0 odczyt przy wycenie; nie drugi katalog; nie mnożenie kwoty |
| ryzyko oferty | offer_risk | 17.0 odczyt; 87.0 wskazanie recenzji na wycenie; nie scoring |
| negocjacja oferty | offer_negotiation | 18.0 odczyt; 85.0 wskazanie `channel_quote` na wycenie; nie nowa kwota; nie spread w JS |
| dokument oferty | offer_document | 19.0 podgląd; 72.0 `document_number` + druk 57.0; nie PDF; nie send |
| wycena wsadowa | quotation_batch | 20.0 wiele kodów na jednej lane; nie CSV; nie nowa tabela |
| zapytanie od klienta | customer_inquiry | 21.0 ślad wycen per party; nie tabela RFQ; nie IMAP |
| zapytanie ofertowe | customer_rfq | 67.0 obiekt; 68.0 wycena; 70.0 `commodity_code_id`; nie kwota na RFQ |
| wykrywanie akceptacji | offer_acceptance | 22.0 pending; 86.0 decyzja S11 na `quotation`; nie HITL accept; nie IMAP |
| zapytanie do armatora | carrier_inquiry | 83.0 obiekt buy do `network_member`; Fala O: batch, statusy `queued`/`sent`/`answered`, lane; N5 data ciszy `no_reply_after`; 23.0 ślad `channel_quote`; nie RFQ; nie live HTTP |
| porównanie odpowiedzi | response_comparison | 84.0 zapis `charge` (buy kanał, sell wycena); 24.0 zestawienie na POL/POD; nie odejmuj w JS |
| integracja pocztowa | mail_integration | 25.0 tablica znanych adresów na `/mail`; 64.0 dopina `inbound_message`; nie IMAP |
| wiadomość przychodząca | inbound_message | 64.0 tabela per tenant; 66.0 treść → extract HITL; 78.0/80.0 ingest `graph://` / `imap://` + `external_id`; 79.0 zdarzenie outbox; nie live skrzynka; nie send; nie blob |
| zdarzenie outbox | outbox_event | 79.0 tabela per tenant; kind `inbound_message_saved`; nie Temporal; nie konsument |
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
| zdarzenie obiektu | entity_event | B0a append-only (`inquiry_sent` / `quote_recorded`); nie Temporal |
| przypisanie roli | party_role_assignment | 132.0; wiele ról na jednym `party`; nie osobny kontrahent na rolę |
| JDG | is_sole_trader | 132.0; kredyt tylko HITL recenzją |
| kontrahent nadrzędny | parent_party_id | 132.0; grupa / oddział; FK tenanta |
| ledger predykcji | prediction_ledger | B0b/V1; metryka po fakcie; zakaz „AI przewiduje” bez MAE |
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
| członek sieci | network_member | 82.0 ręczny agent w `network` tenanta; O0 `party_id` FK tenanta; nie portal |
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
| konektor slotu | terminal_slot_connector | T8; mode `api`/`email_hitl`/`portal_task`/`unsupported` per terminal; nie gwarancja |
| awizacja terminalu | terminal_appointment | T8; requested/confirmed/rejected; `source_ref` |
| kalendarz organizacji | organization_calendar | U4; dni robocze; grace GPS |
| przeniesienie pól | field_carry_forward | U1; oferta→zlecenie; nie cichy overwrite |
| reguła checklisty dokumentów | document_checklist_rule | U5; incoterm×strona×mode → rodzaj + blocks_dispatch |
| przesyłka | consignment | N1; obok shipment |
| podłoga marży | margin_floor | N6; Decimal; 409 albo S11 |
| ETA fizyczne | eta_physical | GPS/korek; nie jedyny znacznik |
| ETA prawne | eta_legal | zakaz jazdy, tacho, cutoff |
| umowa klienta | customer_contract | CI; ciphertext; nie super-admin |
| klauzula SLA | sla_clause | CI; wpis ręczny; kara SQL |
| prognoza spóźnienia | delay_forecast | CI4; przed actual late |
| wynik interwencji | intervention_outcome | CI6–CI7; saved = SQL |
| przetarg | tender | G2.0 nagłówek sell/buy; nie P6 `tender_quote`; nie loty |
| partia przetargu | tender_lot | G2.1 kod partii na `tender`; nie korytarz; nie kwota |
| korytarz przetargu | tender_lane | G2.2 para UN/LOCODE na `tender_lot`; nie runda; nie kwota |
| oferta przetargowa kupna | tender_quote | P6 ważność + limit orderów; nie auto-award; nie obiekt `tender` |
| kółko | lane_circle | G2.20–G2.21; nakładanie dat |
| KREPTD | kreptd | G2.23; GITD/ITD; oficjalne API |
| licencja transportowa | transport_licence | party_document; KREPTD |
| sold-to | sold_to_party_id | EXP1; korpo |
| bill-to | bill_to_party_id | EXP1 |
| ship-to | ship_to_party_id | EXP1 |
| haulier faktyczny | actual_haulier_party_id | ≠ booked; double-broker |
| miejsce nazwane | named_place | Incoterms; 409 bez DAP/DDP |
| fabryka demo | demo_sim | Demo-1; nie GBOX klienta |
| zakłócenie demo | demo_disruption | korki/wypadki fixture |
| zużycie platformy | platform_usage_daily | Admin-P; agregat; nie cross-tenant SELECT |
| tenant demo | demo_tenant | izolacja RLS; wipe USUN |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

