# Wyjątek operacyjny

Wycena bez POL/POD to jeszcze nie wyjątek. Wiersz powstaje, gdy go **zapiszesz** na `/exceptions`, na konkretnym zleceniu.

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na wyjątki. Wklej `shipment_id`, rodzaj (`noted`, `blocked` albo `other`) i `source_ref` (`fixture://operational-exception/…` albo `tenant:manual`).
3. „Zapisz wyjątek” wstawia wiersz. System nic nie klasyfikuje. Nie ma mapy.

Czego tu nie ma: AIS, czas przybycia liczony, odcinki, auto-wiersz z brakującego lane, `party_charge_override`.

Nazwy w kodzie: `operational_exception` · `exception_kind` · `source_ref`.
