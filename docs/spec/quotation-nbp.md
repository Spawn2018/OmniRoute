# M-23 waluty w ofercie — odczyt `nbp_rate` przy `quotation`

**Moduł żywy:** M-23 (katalog `nbp_rate` z 6.0) + ekran M-21 `quotation`  
**Plaster:** **16.0** (plan)  
**Status:** plan — wycena **czyta** kurs tabeli A. Nie drugi katalog. Nie mnożenie kwoty.

Delta: [docs/deltas/open/16.0-quotation-nbp.md](../deltas/open/16.0-quotation-nbp.md).

## 16.0 kurs przy ofercie

### Zakres

- Na `/quotations`: panel „Kurs NBP waluty oferty” — `resolve` istniejącego `nbp_rate` (waluta + dzień)
- Operator wpisuje ISO z wiersza wyceny (`quotation.currency`) i dzień; wynik to `mid` + `source_ref`
- PLN: komunikat, że katalog 6.0 nie trzyma PLN — bez wywołania resolve
- Zero nowej tabeli. Zero importu `nbp_rates` z `quotations` service (niezależność BC)

### Poza 16.0

Mnożenie `amount * mid` (PLN) · zapis `nbp_rate_id` na `quotation` · drugi katalog kursów · ECB · tabela C · live HTTP NBP · zmiana `charge.margin` · LLM liczący kurs

### HC

- Kwota wyceny zostaje ze `rate_line` (SQL). Kurs to odczyt katalogu.
- LLM nie liczy. Decimal zostaje na `nbp_rate.mid`.
- ExtractionService nie importuje rates / quotations
