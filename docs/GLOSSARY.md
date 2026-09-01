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
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| zlecenie | shipment | handlowe |
| odcinek | shipment_leg | operacyjne |
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
| kurs NBP | nbp_rate | D-1 roboczy |
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
| operator terminalu | operator_name | tekst na `terminal`; FK `operator_party_id` = plaster 5.0 |
| kontrahent | party | katalog M-10; jeden podmiot, wiele ról |
| identyfikator podatkowy | tax_id | NIP / VAT krajowy; `resolve` po tokenie |
| numer VAT UE | vat_eu | opcjonalny; lookup VIES nie zapisuje sam |
| REGON | regon | opcjonalny |
| KRS | krs | opcjonalny |
| role kontrahenta | party roles | `customer` `vendor` `agent` `carrier` `shipper` `consignee` `notify` |
| kontakt kontrahenta | party_contact | bez portalu w 5.0 |
| rachunek kontrahenta | party_bank_account | IBAN; `whitelist_status` z lookupu |
| domena mailowa kontrahenta | party_email_domain | katalog; matcher maili = M-11 |
| wyjątek stawki kontrahenta | party_charge_override | katalog uzgodnień; nie silnik wyceny / nie marża |
| profil armatora | carrier_profile | 1:1 z `party`; adapter tylko jako dane |
| numer WPI | wpi_number | World Port Index (NGA Pub 150) na `port` |
| wielkość portu | harbor_size | WPI: Very Small / Small / Medium / Large |
| typ portu | harbor_type | WPI, słownik NGA |
| schronienie | shelter | WPI: Excellent / Good / Fair / Poor / None |
| głębokość toru | channel_depth_m | WPI, metry, Numeric |
| głębokość nabrzeża | cargo_pier_depth_m | WPI, metry, Numeric |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

