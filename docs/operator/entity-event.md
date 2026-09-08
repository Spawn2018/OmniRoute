# Zdarzenie podmiotu

Na `/entity-events` dopisujesz wpis do dziennika: jaki obiekt (`carrier_inquiry`, `quotation`, `channel_quote`), jaki rodzaj (`inquiry_queued`, `inquiry_sent`, `quote_recorded`) i skąd wiesz (`source_ref`). To nie outbox i nie wylicza oferty.

Ten sam obiekt może mieć wiele wpisów. Nie ma poprawiania ani kasowania wiersza. Nie ma kwoty na tym ekranie.
