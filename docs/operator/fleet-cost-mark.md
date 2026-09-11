# Fleet cost (EXP2.15)

Operator zapisuje etykietę kosztu floty: TCO, utrzymanie, leasing albo inny. To
katalog HITL, nie kalkulator TCO.

Wiersz ma `mark_code`, `cost_kind` i `source_ref`. System nie sumuje kosztów, nie
łączy z CMMS work_order i nie tworzy charge. Osobny katalog `cmms_mark` (G7)
obsługuje rodzaje work_order/DTC.

Live fleet cost / TCO SQL zostają leftoverem poza tym plasterem.
