# Operator: znacznik webhook outbox

Katalog HITL dla protokołu webhook outbox (pojedynczy / paczka / ręczny).
Zapisujesz kod, rodzaj i `source_ref`. To nie woła live webhook hubu ani Temporal.

`amount` i bajty są odrzucane. Zmiana wiersza = nowy rekord (brak UPDATE).
