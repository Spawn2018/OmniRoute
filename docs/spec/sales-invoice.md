# M-40 fakturowanie — tabela na zleceniu

**Moduł żywy:** M-40 (tabela `sales_invoice`) + ekran M-08 `charge`  
**Plaster:** **97.0** (S35) po **96.0** / **33.0**  
**Status:** operator **zapisuje** fakturę na `shipment` i **dopisuje numer sesji** KSeF. Kwoty zostają na `charge`. Nie live HTTP.

Delta: [docs/deltas/archived/97.0-ksef-ref.md](../deltas/archived/97.0-ksef-ref.md). Tabela: [docs/deltas/archived/96.0-sales-invoice.md](../deltas/archived/96.0-sales-invoice.md). Fundament: [docs/deltas/archived/33.0-sales-invoice.md](../deltas/archived/33.0-sales-invoice.md).

## 33.0 tablica odczytu na `/invoices`

Zastąpiona w 96.0. Historycznie: lista `sell_amount` z `charge` bez tabeli.

## 96.0 tabela na `/invoices`

### Zakres

- Tabela `sales_invoice` per tenant, FK do `shipment`, RLS FORCE
- Ekran `/invoices`: lista wierszy + „Zapisz fakturę”. Link do `/charges`, `/finance` i `/shipments`
- `invoice_kind` `issued` | `noted` | `other`. `invoice_ref` wpisany przez operatora. `source_ref` obowiązkowy

### Poza 96.0

KSeF (97.0) · licznik numeru · kwota / marża na wierszu · M-41 rozliczenie · PDF · F9.1

## 97.0 numer sesji na `/invoices`

### Zakres

- Kolumny `ksef_ref` i `ksef_noted_at` na `sales_invoice`
- `POST /sales-invoices/{id}/note-ksef` — operator wpisuje numer, który już ma
- Prefix `fixture://ksef/` albo `ksef://`. Ten sam ekran, druga akcja

### Poza 97.0

Live HTTP do MF · XML / FA(3) · licznik numeru · M-41 · PDF · F9.1

### HC

- Marża zostaje w `charge`. Wiersz faktury nie niesie kwoty.
- LLM nie pisze treści faktury ani numeru sesji.
- HITL zostaje na ekstrakcji.
- ExtractionService nie importuje faktur
- Serwis nie woła sieci; brak XML / FA(3)
