# Przetarg

Na `/tenders` zapisujesz **nagłówek** przetargu: strona sell/buy, rodzaj, status, nabywcę, termin i Incoterms jako dane. To nie loty i nie auto-award.

1. Wejdź na Przetargi. Wklej `party_id` nabywcy tenanta.
2. Podaj `side`, `kind`, `status`, dzień `deadline_at`, Incoterm i stronę handlu.
3. DAP/DDP wymaga miejsca. „Zapisz przetarg” z `source_ref` (`fixture://tender/…` albo `tenant:manual`).

Czego tu nie ma: loty G2.1, auto-award, kwota na tym wierszu. Marża zostaje na `/charges`. Oferta kupna zostaje na `/tender-quotes`.

Nazwy w kodzie: `tender` · `side` · `kind` · `status` · `buyer_party_id` · `deadline_at` · `incoterm` · `trade_side` · `named_place` · `source_ref`.
