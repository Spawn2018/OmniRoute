# BC groupage_dispatcher_mark (BR3.2)

HITL katalog znacznika dyspozytora drobnicy per tenant. mark_code +
dispatcher_kind line|hub|cutoff|consol|other + source_ref. Nie silnik hubów.
Nie live.

## Dozwolone zaleznosci
- `app.models.groupage_dispatcher_mark`
- `app.repositories.groupage_dispatcher_marks`
- `app.domain`

## Zakaz
- import innych BC services (groupage_lines, groupage_tariffs, cutoff_marks, charges, extraction)
- zapis `groupage_line` / `groupage_tariff` / `cutoff_mark` / `charge`
- silnik hubów / OR konsolidacji / matching cutoff SQL
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
- FK do `groupage_line` / `shipment` / `consignment` / `stop`
