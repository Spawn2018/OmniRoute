# Powiadomienie o klauzuli (CI3)

Operator zapisuje katalogowe powiadomienie o klauzuli: kod, etykietę klauzuli (tekst)
i `source_ref`. To dane HITL, nie HTTP 409 na operacji i nie auto-kara na FV.

Nie wiąże FK do `sla_clause`. Nie zapisuje `charge`. Marża nadal tylko na `charge`.

Ścieżka UI: `/clause-notices`.
