# Opcja MQC okno na wycenie (655.0)

Na `/quotations` operator może podać opcjonalne `mqc_window` (tekst 1–64, np. `CY2026`) przy tworzeniu oferty albo później przez PATCH `…/mqc-window`.

To jest HITL — system nie liczy zakresu dat, nie mnoży MQC vs actual i nie tworzy `charge`. Puste pole = brak etykiety okna na wierszu.
