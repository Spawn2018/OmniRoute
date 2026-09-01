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
| terminal | terminal | 4.2; ISPS na terminalu |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

