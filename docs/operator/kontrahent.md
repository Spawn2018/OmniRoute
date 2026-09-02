# Kontrahent

Lookup po NIP albo VIES **nie zapisuje** karty. Dostajesz szkic. Zapis `party` jest dopiero po twoim potwierdzeniu — ten sam `tax_id` i kraj, nie luźna nazwa.

1. Wejdź na katalog kontrahentów. Szukaj po numerze podatkowym, nie po nazwie z maila.
2. Lookup (GUS/VIES/whitelist w CI to fixture) pokazuje propozycję. To nie jest wiersz w bazie.
3. Potwierdź i zapisz. Dopiero wtedy powstaje `party` z `source_ref`.
4. Kontakty, IBAN i domeny maila dopinasz do **tej** karty. Matcher maila sam nic nie wstawia.
5. Uzgodnienie stawki (`party_charge_override`) siedzi na karcie. Marża i tak liczy się na `charge`, nie tutaj.
6. Ocena kredytowa to recenzja z decyzją, nie automatyczny scoring osoby.

Czego tu nie ma: live GUS w CI, tuple OpenFGA na wiersz, auto-limit kredytowy.

Nazwy w kodzie: `party` · `resolve(tax_id)` · `lookup` = szkic.
