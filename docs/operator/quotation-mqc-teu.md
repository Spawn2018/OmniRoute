# Opcja MQC TEU na wycenie (654.0)

Na `/quotations` operator może podać opcjonalne `mqc_teu` (Decimal ≥ 0) przy tworzeniu oferty albo później przez PATCH `…/mqc-teu`.

To jest HITL — system nie liczy MQC vs actual i nie tworzy `charge`. Puste pole = brak zobowiązania TEU na wierszu.
