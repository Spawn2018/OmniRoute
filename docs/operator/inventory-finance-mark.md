# Zapas finansowy (BR1.2)

Operator zapisuje katalogowy stance zapasu jako obiektu finansowego: kod,
`finance_kind` (`valuation` / `aging` / `release` / `other`) i `source_ref`.
To dane HITL — nie silnik wyceny SQL, nie wiekowanie w bazie ani wartość
towaru.

Nie liczy kwot. Marża nadal tylko na `charge`. Pozycja WMS zostaje w
`inventory_position_mark`; finansowanie PO w `po_financing_mark`.

Ścieżka UI: `/inventory-finance-marks`.
