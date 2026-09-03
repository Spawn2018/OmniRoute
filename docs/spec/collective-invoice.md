# M-91 zbiorcza faktura — dodatkowe zlecenie na fakturze

**Moduł żywy:** M-91 (tabela `collective_invoice`)  
**Plaster:** **105.0** (S43)  
**Status:** operator **zapisuje**, że ta faktura obejmuje jeszcze to zlecenie. Kotwica zostaje na `sales_invoice.shipment_id`. Kwoty zostają na `charge`. Nie JPK.

Delta: [docs/deltas/open/105.0-collective-invoice.md](../deltas/open/105.0-collective-invoice.md).

## 105.0 tabela `collective_invoice`

### Zakres

- Tabela `collective_invoice`: `sales_invoice_id` + `shipment_id` + `source_ref`
- `GET/POST /collective-invoices`, OpenFGA `can_manage_collective_invoices`
- Ekran `/invoices`: lista członków + „Zapisz zbiorczą”
- Zero kwoty na wierszu. To samo `party_id` co kotwica.

### Poza 105.0

Płatność paczką · JPK · PDF · live KSeF · druga marża

### HC

- Marża zostaje w `charge`. Wiersz nie sumuje zleceń.
- LLM nie liczy zbiorczej.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje collective_invoice / sales_invoices
