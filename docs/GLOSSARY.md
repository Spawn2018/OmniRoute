# Słownik domenowy PL / EN

| PL | EN (kod) | Uwagi |
|---|---|---|
| stawka | rate_line | niemutowalna, source_ref |
| opłata / charge | charge / shipment_charge | jedyne miejsce prawdy o marży |
| kod opłaty | charge_code | katalog M-06; typowany token, nie luźny string |
| alias kodu opłaty | charge_code alias | synonim w katalogu tenanta |
| wycena | quotation | |
| luka wyceny | quotation_gap | brakująca dopłata |
| zlecenie | shipment | handlowe |
| odcinek | shipment_leg | operacyjne |
| tenant | organization | organization_id wszędzie |
| token sesji | session token | JWT HS256; claims `sub` + `org` |
| token odświeżający | refresh_token | rotacja; RLS; nie access JWT |
| skrót hasła | password_hash | argon2id; nigdy plaintext w API |
| pochodzenie | source_ref | obowiązkowe |
| szkic ekstrakcji | extraction_draft | HITL przed zapisem domeny |
| region nierozpoznany | unparsed_region | zawsze w payloadzie ekstrakcji |
| odcisk układu | layout_fingerprint | pdf vs text przed parserem |
| delta A/B parsera | ab_delta_chars | różnica długości tekstu A vs B (0.9) |
| kurs NBP | nbp_rate | D-1 roboczy |
| narzut | markup | kaskada — Python mały zbiór (DECISIONS) |
| pieniądze | money | para `amount` + `currency`; nigdy float |
| kwota | amount | `Decimal` / tekst dziesiętny, skala Numeric(14,4) |
| waluta | currency | ISO 4217 CHAR(3), nierozerwalnie z kwotą |

Pełny słownik archiwalny: `Informacje z claude/OmniRoute-dokumentacja/docs/` — **nie dumpować**; uzupełniaj ten plik przy plastrze.

