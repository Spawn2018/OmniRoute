# M-40 fakturowanie — tabela na zleceniu

**Moduł żywy:** M-40 (tabela `sales_invoice`) + ekran M-08 `charge`  
**Plaster:** **96.0** (S34) po fundamencie **33.0**  
**Status:** operator **zapisuje** fakturę na `shipment`. Kwoty zostają na `charge`. Nie KSeF.

Delta: [docs/deltas/archived/96.0-sales-invoice.md](../deltas/archived/96.0-sales-invoice.md). Fundament: [docs/deltas/archived/33.0-sales-invoice.md](../deltas/archived/33.0-sales-invoice.md).

## 33.0 tablica odczytu na `/invoices`

Zastąpiona w 96.0. Historycznie: lista `sell_amount` z `charge` bez tabeli.

## 96.0 tabela na `/invoices`

### Zakres

- Tabela `sales_invoice` per tenant, FK do `shipment`, RLS FORCE
- Ekran `/invoices`: lista wierszy + „Zapisz fakturę”. Link do `/charges`, `/finance` i `/shipments`
- `invoice_kind` `issued` | `noted` | `other`. `invoice_ref` wpisany przez operatora. `source_ref` obowiązkowy

### Poza 96.0

KSeF · licznik numeru · kwota / marża na wierszu · M-41 rozliczenie · PDF · F9.1

### HC

- Marża zostaje w `charge`. Wiersz faktury nie niesie kwoty.
- LLM nie pisze treści faktury.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje faktur
