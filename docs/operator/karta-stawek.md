# Karta stawek

Na `/rate-cards` zapisujesz **warunek** (`applies_when`) i kwotę Decimal. To nie silnik WHEN/IF i nie stawka na wycenie.

1. Wejdź na Karty stawek. Podaj `card_code` (snake), tekst warunku i kwotę z walutą ISO.
2. Zero i float na kwocie odpadają. Pusty warunek odpada.
3. „Zapisz kartę stawek” z `source_ref` (`fixture://rate-card/…` albo `tenant:manual`).
4. „Dopasuj warunek” pokazuje karty, których `applies_when` jest **dokładnie** taki jak wpisałeś (równość SQL). To nie dopisuje opłaty ani marży.

Czego tu nie ma: parser WHEN/IF/CALC, daty ważności / exclusion, FSC, zapis na `charge` albo `rate_line`. Marża zostaje na `/charges`. Extra portowe zostają na `/port-surcharges`.

Nazwy w kodzie: `rate_card` · `card_code` · `applies_when` · `amount` · `currency` · `source_ref`.
