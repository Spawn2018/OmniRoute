# Prognoza opóźnienia (CI4)

Operator zapisuje katalogową prognozę opóźnienia: kod, horyzont w godzinach (1–168),
`p_late` jako Decimal 0–1 i `source_ref`. To dane HITL, nie wróżba punktowa i nie GPS.

Nie liczy ETA. Nie woła AIS. Nie zapisuje `charge`. Marża nadal tylko na `charge`.

Ścieżka UI: `/delay-forecasts`.
