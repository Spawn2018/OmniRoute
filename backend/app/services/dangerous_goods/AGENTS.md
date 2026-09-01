# BC dangerous_good (M-52)

Katalog numeru UN + klasy IMDG — nie `charge`, nie podpięcie do wyceny.

## Dozwolone zależności
- `app.models.dangerous_good`
- `app.repositories.dangerous_goods`
- `app.domain`

## Zakaz
- import innych BC services
- zapis `quotation` / `commodity_code` / `charge`
- nadawanie klasy przez LLM
