# BC eur1_atr_mark (EXP3.7)

HITL katalog znacznika EUR.1/ATR per tenant. mark_code + cert_kind
eur1|atr|origin|other + source_ref. Nie EUR.1 live. Nie ATR scrape.

## Dozwolone zaleznosci
- `app.models.eur1_atr_mark`
- `app.repositories.eur1_atr_marks`
- `app.domain`

## Zakaz
- import innych BC services (commodity_codes, charges, extraction)
- zapis `commodity_code` / `charge`
- EUR.1 live · ATR scrape · kwota
- HTTP
- UPDATE / DELETE wiersza
