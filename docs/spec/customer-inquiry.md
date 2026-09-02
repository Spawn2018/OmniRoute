# M-28 zapytania od klientów — ślad wycen + obiekt RFQ

**Moduł żywy:** M-28 (`customer_inquiry` ślad · `customer_rfq` obiekt)  
**Plaster:** **67.0** (obiekt) · **21.0** (ślad na wycenach)  
**Status:** operator tworzy zapytanie z wiadomości na `/mail`. Silnik wyceny na RFQ = M-21 68.0. Panel 21.0 na `/quotations` zostaje śladem. Nie IMAP.

Delta: [67.0](../deltas/archived/67.0-customer-rfq.md) · [21.0](../deltas/archived/21.0-customer-inquiry.md).

## 21.0 ślad zapytań z wycen

### Zakres

- Na `/quotations`: panel „Zapytania od klientów” — `party_id` z listy wycen + nazwa z katalogu `party`
- Każda grupa pokazuje kody i kwoty (`<Money/>`) już zapisane na `quotation`
- Zero nowej tabeli. Zero nowego endpointu. Zero sumowania kwot w JS

### Poza 21.0

Tabela RFQ · IMAP (M-32) · status zapytania · auto-INSERT wyceny · M-29 akceptacja · M-30 wysyłka do armatora · LLM

### HC

- Kwota zostaje ze `rate_line` (SQL). Panel nic nie liczy.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- ExtractionService nie importuje quotations

## 67.0 obiekt customer_rfq

### Zakres

- Tabela `customer_rfq` per tenant, FK tenanta do `inbound_message`, jeden RFQ na wiadomość
- `GET/POST /customer-rfqs`, OpenFGA `can_manage_customer_rfqs`
- `/mail`: przycisk „Utwórz RFQ”
- Zero kwoty. Zero silnika wyceny

### Poza 67.0

Silnik na RFQ (68.0) · HS/CN (70.0) · IMAP · zastąpienie panelu 21.0 · auto przy INSERT maila

## 68.0 silnik M-21 na tym RFQ

`quotation.customer_rfq_id`. Kwota ze stawki. `/quotations` picker + `/mail` link Wycena. Nie nowy silnik.

### HC

- Kwota nie wchodzi na RFQ. Silnik wyceny = S5.
- LLM nie liczy. `charge` zostaje prawdą o marży.
- Serwis RFQ nie importuje inbound/quotations

## 70.0 HS/CN

`customer_rfq.commodity_code_id` i `quotation.commodity_code_id`. Katalog M-09. Nie kwota. UN leftover.
