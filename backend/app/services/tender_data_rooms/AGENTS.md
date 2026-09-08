# BC tender_data_room (G2.4)

Pokój danych per tenant. NDA jako dana. Nie extract. Nie bajty. Nie kwota.

## Dozwolone zależności
- `app.models.tender_data_room`
- `app.repositories.tender_data_rooms`
- `app.domain`

## Zakaz
- import innych BC services (tenders, tender_rounds, quotations, charges)
- zapis `tender` / `tender_round` / `charge`
- bajty / extract RFP / kwota / marża / float
- HTTP / tuple OpenFGA per plik
