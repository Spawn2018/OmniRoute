# Memory — tablica-odczyt vs moduł

Najczęstszy błąd oceny: trasa + filtr cudzego API traktowana jak ukończony BC. W repo jest ~27 takich tablic. Agent kopiuje najliczniejszy wzorzec.

## Trzy pytania

1. Czy jest **własna tabela** z `organization_id` i RLS FORCE?
2. Czy ten BC ma **własny zapis** (POST/serwis), nie tylko SELECT cudzego wiersza?
3. Czy jest **test izolacji** tenantów na tej tabeli?

Jeśli którekolwiek „nie” — to tablica-odczyt albo nakładka. **Nie idzie na notę 5,0.** Leftover w docs-debt, nie „moduł gotowy”.

## Anty-wzorzec

Nie kopiuj `/shipments`, `/tracking`, `/invoices` jako szablonu nowego katalogu. Wzorzec katalogu: M-01 tenancy, M-07 `rate_line`, M-08 `charge`.
