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
| kod towarowy | commodity_code | katalog M-09; token HS/CN cyframi; nie luźna nazwa |
| towar niebezpieczny | dangerous_good | katalog M-52; token UN czterema cyframi; nie luźna nazwa |
| numer UN | un_number | 4 cyfry na `dangerous_good`; prefiks UN zbędny |
| klasa IMDG | imdg_class | allowlista 1–9 z podziałem (2.1, 4.1, …); nie packing group |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| port załadunku | origin_port_id | POL na `quotation`; FK do `port` |
| port wyładunku | destination_port_id | POD na `quotation`; FK do `port` |
| zlecenie | shipment | 28.0 tablica wycen z `party_id`; nie tabela; nie tracking |
| śledzenie | tracking | 29.0 tablica lane POL/POD z wyceny; nie AIS; nie mapa |
| wyjątek operacyjny | operational_exception | 30.0 tablica wycen z party bez pełnego POL/POD; nie tabela; nie AIS; nie `party_charge_override` |
| dokument zlecenia | shipment_document | 31.0 tablica `source_ref` wycen z party; nie tabela; nie PDF; nie HBL |
| komunikat EDI | edi_message | 32.0 tablica `channel_quote` na lane wyceny; nie tabela; nie X12; nie live HTTP |
| faktura sprzedaży | sales_invoice | 33.0 tablica `sell` z `charge`; nie tabela; nie KSeF; nie druga marża |
| rozliczenie wyceny z fakturą | quote_invoice_settlement | 34.0 tablica wycena + `sell` z `charge` po `rate_line_id`; nie tabela; nie odejmowanie |
| bank i płatności | bank_payment | 35.0 tablica IBAN + `sell` z `charge`; nie tabela płatności; nie SEPA |
| koszt pieniądza | money_cost | 36.0 tablica NBP + `buy` z `charge`; nie tabela odsetek; nie mnożenie |
| różnica kursowa | fx_difference | 37.0 tablica NBP walut z `charge`/`quotation`; nie tabela; nie przeliczenie |
| przepływ | cash_flow | 38.0 tablica `buy`/`sell` z `charge` jako wypływ/wpływ; nie tabela księgi; nie odejmowanie |
| koszt obsługi klienta | cost_to_serve | 39.0 tablica SOP + wyceny kontrahenta; nie tabela ABC; nie suma |
| księgowość | bookkeeping | 40.0 tablica `charge` + `charge_code.name`; nie JPK; nie ERP |
| transport drogowy | road_transport | 41.0 tablica `location` `postal_zone`/`address`; nie TMS; nie GPS |
| odcinek | shipment_leg | operacyjne; nie w 29.0 |
| tenant | organization | organization_id wszędzie |
| ustawienie tenanta | organization_setting | konfiguracja jako dane; allowlista kluczy; nie sekret |
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
| ryzyko oferty | offer_risk | 17.0 odczyt recenzji i karty przy wycenie; nie tabela; nie scoring |
| negocjacja oferty | offer_negotiation | 18.0 odczyt `channel_quote` przy wycenie; nie tabela wyniku; nie spread w JS |
| dokument oferty | offer_document | 19.0 podgląd faktów `quotation`; nie PDF; nie U-print |
| wycena wsadowa | quotation_batch | 20.0 wiele kodów na jednej lane; nie CSV; nie nowa tabela |
| zapytanie od klienta | customer_inquiry | 21.0 ślad wycen per party; nie tabela RFQ; nie IMAP |
| wykrywanie akceptacji | offer_acceptance | 22.0 pending z wycen; nie tabela wyniku; nie HITL accept; nie IMAP |
| zapytanie do armatora | carrier_inquiry | 23.0 ślad `channel_quote` przy lane wyceny; nie tabela RFQ; nie live HTTP |
| porównanie odpowiedzi | response_comparison | 24.0 zestawienie kwot wyceny i `channel_quote` na POL/POD; nie tabela; nie spread w JS |
| integracja pocztowa | mail_integration | 25.0 tablica znanych adresów na `/mail`; nie IMAP; nie tabela skrzynki |
| klient poczty | mail_client | 26.0 `mailto:` z `party_contact.email`; nie dodatek Office; nie Graph |
| powiadomienie operatora | operator_notice | 27.0 tablica HITL pending i wycen pending; nie tabela; nie wysyłka |
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
| opłata portowa warunkowa | port_surcharge | M-18; katalog extra per `port`; warunek to dane; nie `charge.margin` |
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
| dopasowanie maila | resolve_email | M-11; domena z adresu → `party`; nie IMAP |
| wyjątek stawki kontrahenta | party_charge_override | katalog uzgodnień; nie silnik wyceny / nie marża |
| profil armatora | carrier_profile | 1:1 z `party`; adapter tylko jako dane |
| sieć spedycyjna | network | katalog M-12; token kodu (`wca`, `fiata`, …); kopia per tenant; nie scraping |
| kod sieci | network code | snake 2–32; `resolve` po kodzie albo aliasie |
| karta wyników kontrahenta | party_scorecard | M-13; snapshot wskaźników per `party`; nie scoring osoby; nie silnik RFQ |
| recenzja kredytowa | credit_review | M-14; decyzja operatora per `party`+dzień; nie auto-scoring; nie `credit_limit` |
| tablica finansowa | finance_board | M-15; odczyt istniejących faktów (`charge.margin`, NBP, limit, recenzja); LLM nie liczy |
| wskaźnik odpowiedzi | response_rate | 0–1 Numeric na karcie; NULL = nieznany |
| mediana czasu odpowiedzi | median_response_hours | godziny Numeric na karcie |
| pozycja cenowa | price_position | 0–1 Numeric na karcie partii w 10.0; per lane = leftover |
| procedura operacyjna klienta | customer_sop | M-16; katalog per `party`; draft/zatwierdzenie; nie generator zadań |
| numer WPI | wpi_number | World Port Index (NGA Pub 150) na `port` |
| wielkość portu | harbor_size | WPI: Very Small / Small / Medium / Large |
| typ portu | harbor_type | WPI, słownik NGA |
| schronienie | shelter | WPI: Excellent / Good / Fair / Poor / None |
| głębokość toru | channel_depth_m | WPI, metry, Numeric |
| głębokość nabrzeża | cargo_pier_depth_m | WPI, metry, Numeric |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

