# Faktura zakupu (F10)

Operator zapisuje HITL numer faktury zakupu: `invoice_ref`, `invoice_kind`
(`noted` / `other`) i `source_ref`. To dane ingestu, nie ranking SQL
i nie auto-link do `charge`.

Nie liczy kwot. Marża nadal tylko na `charge`.

Ścieżka UI: `/purchase-invoices`.
