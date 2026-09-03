# M-30 zapytania do agentów — obiekt `carrier_inquiry`

**Moduł żywy:** M-30 `carrier_inquiry` + ekran M-12 `/networks` + ślad 23.0 na M-21 `/quotations`  
**Plaster:** **83.0** (zamknięty) · 23.0 ślad (zamknięty)  
**Status:** operator **zapisuje** zapytanie do członka sieci. Panel 23.0 nadal pokazuje oferty kanału przy lane. Nie wysyłka HTTP.

Delta: [docs/deltas/archived/83.0-carrier-inquiry.md](../deltas/archived/83.0-carrier-inquiry.md).

## 83.0 obiekt buy

### Zakres

- Tabela `carrier_inquiry`: FK tenanta do `network_member`, status `draft`, `source_ref`
- `GET/POST /carrier-inquiries`, OpenFGA `can_manage_networks`
- Na `/networks`: `data-carrier-inquiry="catalog"` — wybór członka i „Zapisz zapytanie”
- Zero kwoty. Zero live HTTP

### Poza 83.0

Live HTTP / S21 · porównanie M-31 · `customer_rfq` · FK quotation/party · scraping

### HC

- Serwis `carrier_inquiries` nie importuje `networks` / `quotations` / `channel_quotes`
- Nieznany członek = FK → 400
- LLM nie liczy. `charge` zostaje prawdą o marży
- 23.0 panel na `/quotations` zostaje śladem `channel_quote`

## 23.0 ślad z katalogu kanału

Na `/quotations`: `data-carrier-inquiry="trail"` — `fetchChannelQuotes` + dopasowanie do lane. Kwota przez `<Money/>`. Zero odejmowania.
