# Odpady BDO / KPO / WSR (waste_mark)

Katalog HITL stancji odpadów per tenant. Operator zapisuje kod snake
(`bdo_01`) oraz rodzaj: `bdo`, `kpo`, `wsr` albo `other`, z obowiązkowym
`source_ref` (`tenant:manual` albo `fixture://waste-mark/…`).

Zapis jest append-only: błąd w rodzaju albo źródle = nowy wiersz, nie
edycja. Lista pokazuje tylko rekordy własnej organizacji (RLS).

To nie jest live MOS / BDO HTTP i nie ustawia kolumny `shipment.is_waste`.
Nie ma kwoty, float ani scoringu. Uprawnienie OpenFGA:
`can_manage_waste_marks`.

Ścieżka UI: `/waste-marks`. API: `GET/POST /api/v1/waste-marks`.
