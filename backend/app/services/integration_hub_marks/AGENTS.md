# BC integration_hub_mark (EXP2.22)

HITL katalog znacznika protokolu Integration Hub per tenant. mark_code + hub_kind
rest|soap|edi|sftp|other + source_ref. Nie live HTTP. Nie Selenium.
Obok erp_connectors / telematics_connectors — tu protokol hubu, nie adapter.

## Dozwolone zaleznosci
- `app.models.integration_hub_mark`
- `app.repositories.integration_hub_marks`
- `app.domain`

## Zakaz
- import innych BC services (erp_connectors, telematics_connectors, charges, extraction)
- zapis `erp_connector` / `telematics_connector` / `charge` / `extraction_draft`
- live HTTP · Selenium portal · nowy silos WMS
- kwota / marza / float
- HTTP
- UPDATE / DELETE wiersza
