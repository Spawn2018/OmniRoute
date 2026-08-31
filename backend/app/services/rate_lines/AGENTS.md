# BC rate_line (M-07)

Niemutowalna stawka kupna + `source_ref`. Nie tabela `charge`, nie accept HITL.

## Dozwolone zależności
- `app.models.rate_line`
- `app.repositories.rate_lines`
- `app.repositories.charge_codes` — odczyt katalogu, nie zapis
- `app.domain`

## Zakaz
- import innych BC services
- zapis `charge` / marża
- zapis z `ExtractionService`
- mutacja `amount` / `currency` / `source_ref` w miejscu
