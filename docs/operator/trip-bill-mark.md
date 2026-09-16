# Gotowość przejazdu do FV (N2)

Operator zapisuje znacznik gotowości per przejazd: kod, `bill_kind`
(`ready` / `held` / `billed` / `other`) i `source_ref`. To dana HITL,
nie widok SQL `trips_to_bill` i nie live KSeF.

Nie liczy kwot. Marza nadal tylko na `charge`.

Sciezka UI: `/trip-bill-marks`.
