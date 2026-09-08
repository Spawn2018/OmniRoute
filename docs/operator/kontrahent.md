# Kontrahent

Lookup po NIP albo VIES **nie zapisuje** karty. Dostajesz szkic. Zapis `party` jest dopiero po twoim potwierdzeniu — ten sam `tax_id` i kraj, nie luźna nazwa.

1. Wejdź na katalog kontrahentów. Szukaj po numerze podatkowym, nie po nazwie z maila.
2. Lookup (GUS/VIES/whitelist w CI to fixture) pokazuje propozycję. To nie jest wiersz w bazie.
3. Potwierdź i zapisz. Nowy wiersz wymaga NIP albo VAT UE albo EORI albo DUNS. Klient bez NIP = odmowa. Ten sam token w firmie = konflikt z linkiem do istniejącej karty. Stare karty mogą nie mieć numeru. Dopiero wtedy powstaje `party` z `source_ref`.
4. Kontakty, IBAN i domeny maila dopinasz do **tej** karty. Matcher maila sam nic nie wstawia.
5. Uzgodnienie stawki (`party_charge_override`) siedzi na karcie. Marża i tak liczy się na `charge`, nie tutaj.
6. Ocena kredytowa to recenzja z decyzją, nie automatyczny scoring osoby.
7. Na `/sanctions` widzisz aktywnych kontrahentów (`tax_id` i kraj). „Zapisz sprawdzenie” dopina URI listy, którą już masz (`fixture://sanctions/` albo `eu://`) do karty `party`. To nie pobiera listy z sieci i nie oznacza automatycznego trafienia. Pochodzenie karty (`source_ref`) i limit kredytowy zostają. Puste albo obce wskazanie jest odrzucane.
8. Na `/party-scorecards` snapshot KPI wpisujesz ręcznie. Sekcja decyzji oferty **czyta** przyjęte i odrzucone wyceny z szyny S11. Nie liczy wskaźnika i nie ocenia osoby.

Czego tu nie ma: live GUS w CI, tuple OpenFGA na wiersz, auto-limit kredytowy, live lista sankcji, auto-match.

JDG zaznaczasz na karcie — wtedy limitu kredytu nie wpisujesz przy zapisie; recenzja zostaje osobnym HITL. Oddział wskazuje `parent_party_id`. Rola `subcontractor` to ta sama lista ról, nie osobna szafa.

Nazwy w kodzie: `party` · `resolve(tax_id)` · `lookup` = szkic.
