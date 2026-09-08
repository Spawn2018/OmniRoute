# M-19 channel_quote — stawka z kanału armatora

**Moduł żywy:** M-19 (archiwum M-19; nie koliduje z żywym M-07 `rate_line` / M-08 `charge`)  
**Plaster:** **13.0** (zamknięty) · **134.0** O1 `transit_days` · **135.0** O2 zapis z wyceny  
**Status:** katalog oferty z kanału per `party`+POL/POD. Nie live HTTP. Nie zapis do `rate_line` / `charge`.

Delta: [docs/deltas/archived/13.0-channel-quote.md](../deltas/archived/13.0-channel-quote.md).

## 13.0 katalog oferty z kanału

### Zakres

- Tabela `channel_quote` per tenant: `organization_id`, `party_id` (armator z `carrier_profile`), `origin_port_id`, `destination_port_id`, `quote_date`, `amount` Numeric(14,4) + `currency` CHAR(3), `source_ref`, timestamps
- Unikat `(organization_id, party_id, origin_port_id, destination_port_id, quote_date)`
- `resolve(party_id, origin_port_id, destination_port_id, on_date)` — najnowszy `quote_date <= on_date`
- OpenFGA `can_manage_rate_lines` = member (kupno z kanału, nie marża)
- UI `/channel-quotes`
- `carrier_profile.api_adapter` zostaje etykietą z 5.0 — **nie** druga tabela adaptera

### Poza 13.0

HTTP do Maersk/Hapag/CMA/MSC · sekrety API · IMAP `rate_source_email` · INSERT `rate_line` / `charge` · DCSA live · M-32 poczta · ExtractionService · LLM liczący kwotę

## 134.0 czas tranzytu i znaczki

Kolumna `transit_days` (int ≥ 1, NULL na starych). `is_cheapest` / `is_fastest_tt` liczy SQL w grupie lane+dzień+waluta. Nie kolumny. Nie NBP.

## 135.0 zapis z wyceny

POST tego samego katalogu. `source_ref = tenant:manual:{user_id}`. Unikat dnia → 409. Formularz na `/quotations`. Nie mutacja kwoty. Nie `rate_line`.

### HC

- RLS FORCE + test izolacji
- `charge` zostaje jedynym miejscem prawdy o marży
- `rate_line` zostaje niemutowalną stawką kupna — tu jest katalog oferty z kanału, nie supersede
- Kwota Decimal, waluta nierozerwalnie; nigdy float
- ExtractionService nie importuje `channel_quotes` / `rate_lines` / `charges`
- LLM nie liczy
- Brak szyfrowania sekretów w tym plasterze — nie ma jeszcze magazynu kluczy tenanta
