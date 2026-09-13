# Faktoring — partner (BR5.0)

Operator zapisuje katalogowy konektor partnera faktoringowego: kod,
`system_kind` (`smeo` / `other`) i `source_ref`. To dane HITL, nie live
HTTP SMEO i nie workflow wypłaty F7.

Nie liczy kwot. Marża nadal tylko na `charge`. Faktura sprzedaży i płatność
bankowa zostają w M-40 / M-42 bez kleju do tego katalogu.

Ścieżka UI: `/factoring-connectors`.
