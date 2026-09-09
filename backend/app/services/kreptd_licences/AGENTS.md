# BC kreptd_licence (G2.23)

HITL numer licencji KREPTD/GITD per tenant. licence_no + source_ref na party. Nie scrape. Nie Citizen API. Nie marża.

## Dozwolone zależności
- `app.models.kreptd_licence`
- `app.repositories.kreptd_licences`
- `app.domain`

## Zakaz
- import innych BC services (parties, tenders, charges, extraction)
- zapis `party` / `party_document` / `charge` / `tender`
- scrape kreptd.gitd.gov.pl / Citizen API / HTTP / LLM / kwota / marża / float
- scoring osoby / kolumny na `party`
