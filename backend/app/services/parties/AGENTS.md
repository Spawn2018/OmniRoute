# BC party (M-10)

Katalog kontrahenta per tenant: `party` i tabele zależne.
`resolve` po `tax_id` — nie luźna nazwa. Lookup GUS/VIES/whitelist zwraca szkic.

## Dozwolone zależności
- `app.models.party`
- `app.models.party_contact`
- `app.models.party_bank_account`
- `app.models.party_email_domain`
- `app.models.party_charge_override`
- `app.models.carrier_profile`
- `app.repositories.parties`
- `app.domain`

## Zakaz
- import innych BC services (w tym `charge_codes`, `charges`, `quotations`)
- zapis z lookupu — INSERT tylko po potwierdzeniu operatora
- sieć w CI — `PARTY_LOOKUP_BACKEND=fixture`
- liczenie kwot / marży / scoringu
