# BC tender_matrix_cell (G2.5)

Komórka matrycy per tenant. Kwota Decimal z P. Nie LLM. Nie druga marża.

## Dozwolone zależności
- `app.models.tender_matrix_cell`
- `app.repositories.tender_matrix_cells`
- `app.domain`

## Zakaz
- import innych BC services (tenders, charges, rate_lines, quotations)
- zapis `tender` / `charge` / `rate_line`
- mapowanie kolumn Excel / extract RFP
- marża / float / HTTP
