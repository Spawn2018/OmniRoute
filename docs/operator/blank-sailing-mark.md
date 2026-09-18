# Blank sailing / congestion / Gate OS (blank_sailing_mark)

Katalog HITL stancji oceanicznych per tenant. Operator zapisuje kod snake
(`blank_01`) oraz rodzaj: `blank`, `congestion`, `gate` albo `other`, z
obowiązkowym `source_ref` (`tenant:manual` albo `fixture://blank-sailing-mark/…`).

Zapis jest append-only: błąd w rodzaju albo źródle = nowy wiersz, nie
edycja. Lista pokazuje tylko rekordy własnej organizacji (RLS).

To nie jest predykcja blank sailing, countdown N3 ani szkic `charge`.
Nie ma kwoty, float ani scoringu. Uprawnienie OpenFGA:
`can_manage_blank_sailing_marks`.

Ścieżka UI: `/blank-sailing-marks`. API: `GET/POST /api/v1/blank-sailing-marks`.
