# Dedup CRM (BR6.0)

Operator zapisuje stance dedup CRM: kod, `dedup_kind`
(`nip` / `vat` / `email` / `other`) i `source_ref`. To dane HITL,
nie merge SQL i nie cold-send.

Nie liczy kwot. Marża nadal tylko na `charge`.

Ścieżka UI: `/crm-dedup-marks`.
