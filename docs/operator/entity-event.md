# Zdarzenie podmiotu

Na `/entity-events` dopisujesz wpis do dziennika: jaki obiekt (`carrier_inquiry`, `quotation`, `channel_quote`), jaki rodzaj (`inquiry_queued`, `inquiry_sent`, `quote_recorded`) i skąd wiesz (`source_ref`). To nie outbox i nie wylicza oferty. POST zapytania ze statusem `queued` sam dopisuje `inquiry_queued` — szkic `draft` nie.

Ten sam obiekt może mieć wiele wpisów. Nie ma poprawiania ani kasowania wiersza. Nie ma kwoty na tym ekranie.
