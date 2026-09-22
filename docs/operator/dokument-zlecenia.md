# Dokument zlecenia

`source_ref` wyceny to jeszcze nie dokument. Wskazanie powstaje, gdy je **zapiszesz** na `/shipment-documents`, na konkretnym zleceniu.

1. Najpierw zapisz zlecenie na `/shipments`.
2. Wejdź na dokumenty zlecenia. Wklej `shipment_id`, rodzaj (`noted`, `attached`, `other` albo `rod`) i `source_ref` (`fixture://shipment-document/…` albo `tenant:manual`). `rod` to wskazanie dowodu dostawy. `pod` nie jest rodzajem — to skrót portu wyładunku.
3. „Zapisz dokument” wstawia wiersz. Nie wgrywasz pliku. Skan i HITL zostają na ekstrakcji.

Czego tu nie ma: bajty, wydruk, numer listu, auto-wiersz przy zapisie zlecenia, treść z modelu językowego.

Nazwy w kodzie: `shipment_document` · `document_kind` · `source_ref`.
