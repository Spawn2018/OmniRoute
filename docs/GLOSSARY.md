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
| towar niebezpieczny | dangerous_good | katalog M-52; token UN czterema cyframi; nie luźna nazwa |
| numer UN | un_number | 4 cyfry na `dangerous_good`; prefiks UN zbędny |
| klasa IMDG | imdg_class | allowlista 1–9 z podziałem (2.1, 4.1, …); nie packing group |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| port załadunku | origin_port_id | POL na `quotation`; FK do `port` |
| port wyładunku | destination_port_id | POD na `quotation`; FK do `port` |
| zlecenie | shipment | 90.0 tabela z wyceny z `party_id`; nie tracking |
| śledzenie | tracking | 91.0 `tracking_event` na zleceniu; nie AIS; nie mapa |
| wyjątek operacyjny | operational_exception | 93.0 tabela na zleceniu; nie AIS; nie mapa; nie `party_charge_override` |
| wieża | watchtower | 94.0 tablica wyjątków + pending S11 + leniwy panel mapy; nie leaflet; nie AIS; nie nowy M-xx |
| dokument zlecenia | shipment_document | 92.0 tabela na zleceniu; nie bajty; nie PDF; nie HBL |
| komunikat EDI | edi_message | 95.0 tabela na zleceniu; 32.0 leftover tablica kanału; nie parser; nie live HTTP |
| faktura sprzedaży | sales_invoice | 96.0 tabela na zleceniu; 97.0 `ksef_ref` wpisany; nie live HTTP; nie druga marża |
| rozliczenie wyceny z fakturą | quote_invoice_settlement | 98.0 tabela pary wycena+faktura; nie kwota; nie druga marża |
| bank i płatności | bank_payment | 35.0 tablica IBAN + `sell` z `charge`; nie tabela płatności; nie SEPA |
| koszt pieniądza | money_cost | 36.0 tablica NBP + `buy` z `charge`; nie tabela odsetek; nie mnożenie |
| różnica kursowa | fx_difference | 37.0 tablica NBP walut z `charge`/`quotation`; nie tabela; nie przeliczenie |
| przepływ | cash_flow | 38.0 tablica `buy`/`sell` z `charge` jako wypływ/wpływ; nie tabela księgi; nie odejmowanie |
| koszt obsługi klienta | cost_to_serve | 39.0 tablica SOP + wyceny kontrahenta; nie tabela ABC; nie suma |
| księgowość | bookkeeping | 40.0 tablica `charge` + `charge_code.name`; nie JPK; nie ERP |
| transport drogowy | road_transport | 41.0 tablica `location` `postal_zone`/`address`; nie TMS; nie GPS |
| kolej intermodalna | intermodal_rail | 42.0 tablica `port` z flagą `rail`; nie wagon; nie CIM |
| kolej z Chin | china_rail | 43.0 tablica `port` CN z flagą `rail`; nie korytarz; nie HTTP |
| drobnica morska | ocean_lcl | 44.0 tablica `port` z `is_seaport`; nie tabela LCL; nie CFS |
| sankcje | sanctions | 45.0 tablica aktywnych `party`; 89.0 sprawdzenie `sanctions_list_ref` na karcie; nie auto-match; nie live lista |
| RODO | gdpr | 46.0 tablica `app_user` email; nie wniosek; nie usuwanie |
| copilot AI | ai_copilot | 47.0 tablica `extraction_draft` pending; 76.0 `mail_draft` obok extract; 81.0 świadomy mailto; nie czat |
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
| odcinek | shipment_leg | operacyjne; nie w 29.0 |
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
| zapytanie do armatora | carrier_inquiry | 83.0 obiekt buy do `network_member`; 23.0 ślad `channel_quote` przy lane; nie RFQ; nie live HTTP |
| porównanie odpowiedzi | response_comparison | 84.0 zapis `charge` (buy kanał, sell wycena); 24.0 zestawienie na POL/POD; nie odejmuj w JS |
| integracja pocztowa | mail_integration | 25.0 tablica znanych adresów na `/mail`; 64.0 dopina `inbound_message`; nie IMAP |
| wiadomość przychodząca | inbound_message | 64.0 tabela per tenant; 66.0 treść → extract HITL; 78.0/80.0 ingest `graph://` / `imap://` + `external_id`; 79.0 zdarzenie outbox; nie live skrzynka; nie send; nie blob |
| zdarzenie outbox | outbox_event | 79.0 tabela per tenant; kind `inbound_message_saved`; nie Temporal; nie konsument |
| klient poczty | mail_client | 26.0 `mailto:` z `party_contact.email`; 81.0 dispatch zaakceptowanego szkicu; nie dodatek Office; nie Graph HTTP |
| powiadomienie operatora | operator_notice | 27.0 tablica pending; 75.0 tabela inbox; nie filtr wycen; nie wysyłka |
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
| oferta z kanału | channel_quote | M-19; katalog oferty armatora per POL/POD; nie live HTTP; nie `rate_line` |
| operator terminalu | operator_name / operator_party_id | tekst zostaje; FK nullable do `party` od 5.0 |
| kontrahent | party | katalog M-10; jeden podmiot, wiele ról |
| identyfikator podatkowy | tax_id | NIP / VAT krajowy; `resolve` po tokenie |
| numer VAT UE | vat_eu | opcjonalny; lookup VIES nie zapisuje sam |
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
| członek sieci | network_member | 82.0 ręczny agent w `network` tenanta; nie portal; nie FK party |
| karta wyników kontrahenta | party_scorecard | M-13; snapshot wskaźników per `party`; nie scoring osoby; nie silnik RFQ |
| recenzja kredytowa | credit_review | M-14; decyzja operatora per `party`+dzień; 88.0 `bureau_attachment_ref`; nie auto-scoring; nie `credit_limit` |
| decyzja operatora | operator_decision | 74.0 szyna pending/accept/reject; 77.0 `lock_version`; nie HITL extract; nie send |
| tablica finansowa | finance_board | M-15; odczyt istniejących faktów (`charge.margin`, NBP, limit, recenzja); LLM nie liczy |
| wskaźnik odpowiedzi | response_rate | 0–1 Numeric na karcie; NULL = nieznany |
| mediana czasu odpowiedzi | median_response_hours | godziny Numeric na karcie |
| pozycja cenowa | price_position | 0–1 Numeric na karcie partii w 10.0; per lane = leftover |
| procedura operacyjna klienta | customer_sop | M-16; 11.0 katalog; 73.0 `blocks_auto`; nie send; nie generator zadań |
| numer WPI | wpi_number | World Port Index (NGA Pub 150) na `port` |
| wielkość portu | harbor_size | WPI: Very Small / Small / Medium / Large |
| typ portu | harbor_type | WPI, słownik NGA |
| schronienie | shelter | WPI: Excellent / Good / Fair / Poor / None |
| głębokość toru | channel_depth_m | WPI, metry, Numeric |
| głębokość nabrzeża | cargo_pier_depth_m | WPI, metry, Numeric |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

