# BC party (M-10)

Katalog kontrahenta per tenant: `party` i tabele zależne.
`resolve` po `tax_id` albo `resolve_email` po adresie — nie luźna nazwa. Nowy INSERT wymaga tax_id / vat_eu / eori / duns; `customer` wymaga tax_id. Lookup GUS/VIES/whitelist zwraca szkic.
Matcher maila (M-11) nie zapisuje `party_contact`.
Karta wyników (M-13) to snapshot — nie silnik RFQ i nie scoring osoby.

## Dozwolone zależności
- `app.models.party`
- `app.models.party_contact`
- `app.models.party_bank_account`
- `app.models.party_email_domain`
- `app.models.party_charge_override`
- `app.models.carrier_profile`
- `app.models.party_scorecard`
- `app.models.credit_review`
- `app.models.customer_sop`
- `app.repositories.parties`
- `app.domain`

## Zakaz
- import innych BC services (w tym `charge_codes`, `charges`, `quotations`)
- zapis z lookupu — INSERT tylko po potwierdzeniu operatora
- sieć w CI — `PARTY_LOOKUP_BACKEND=fixture`
- liczenie kwot / marży / scoringu / auto-scoringu kredytowego
