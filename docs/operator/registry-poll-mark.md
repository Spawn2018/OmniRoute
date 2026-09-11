# Poll rejestrów (EXP7.2)

Operator zapisuje katalogowy znacznik billingu: kod, `poll_kind`
(`seat` / `usage` / `invoice` / `other`) i `source_ref`. To dane HITL,
nie live scrape, nie notice auto i nie HTTP CEIDG.

Nie liczy kwot. Marża nadal tylko na `charge`.

Ścieżka UI: `/registry-poll-marks`.
