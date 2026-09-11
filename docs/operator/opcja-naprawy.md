# Opcja naprawy (CI6)

Operator zapisuje katalogową opcję naprawy: kod, rodzaj (`rebook` / `wait` /
`claim` / `other`) i `source_ref`. To dane HITL, nie koszt naprawy i nie auto-send
S11.

Nie zapisuje kwoty. Nie liczy „uratowane”. Marża nadal tylko na `charge`.

Ścieżka UI: `/remediation-options`.
