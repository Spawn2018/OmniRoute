# Zdarzenie podmiotu

Na `/entity-events` dopisujesz wpis do dziennika: jaki obiekt (`carrier_inquiry`, `quotation`, `channel_quote`), jaki rodzaj (`inquiry_queued`, `inquiry_sent`, `quote_recorded`) i skąd wiesz (`source_ref`). To nie outbox i nie wylicza oferty. POST zapytania ze statusem `queued` sam dopisuje `inquiry_queued`, ze `sent` — `inquiry_sent`, z `answered` (kwota i waluta) — `quote_recorded`. To samo `quote_recorded` powstaje po akceptacji szkicu `carrier_quote` z `carrier_inquiry_id` (HITL na `/ai`). Szkic `draft` i `declined` nie.

Ten sam obiekt może mieć wiele wpisów. Nie ma poprawiania ani kasowania wiersza. Nie ma kwoty na tym ekranie.
